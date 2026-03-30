"""
Kafka producer and consumer wiring for ticket-service.

Consumers run on the asyncio event loop (Kafka poll in a thread pool) so Motor
can be used safely. See docs/kafka-replication-architecture.md.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from kafka import KafkaConsumer, KafkaProducer

from app.config.app_config import settings
from app.config.mongo_config import get_mongo_database
from app.external.billboard.application.services.billboard_replication_service import (
    BillboardReplicationService,
)
from app.external.billboard.infrastructure.repository.mongo_cinema_repo import (
    MongoCinemaRepository,
)
from app.external.billboard.infrastructure.repository.mongo_showtime import (
    MongoShowtimeRepository,
)
from app.external.billboard.infrastructure.repository.mongo_theater_repo import (
    MongoTheaterRepository,
)
from app.shared.events.infrastructure.kafka_deduplication import KafkaEventDeduplicator
from app.shared.events.infrastructure.kafka_publisher import KafkaEventPublisher
from app.shared.events.infrastructure.noop_publisher import NoopEventPublisher
from app.shared.events.protocols import EventPublisher

logger = logging.getLogger(__name__)

_producer: Optional[KafkaProducer] = None


def create_event_publisher() -> EventPublisher:
    """
    Returns a KafkaEventPublisher when Kafka is configured,
    or a NoopEventPublisher for local / test environments.
    """
    global _producer

    if not settings.KAFKA_ENABLED or not settings.KAFKA_BOOTSTRAP_SERVERS.strip():
        logger.info("Kafka disabled — using no-op event publisher")
        return NoopEventPublisher()

    if _producer is None:
        servers = [s.strip() for s in settings.KAFKA_BOOTSTRAP_SERVERS.split(",") if s.strip()]
        _producer = KafkaProducer(
            bootstrap_servers=servers,
            client_id=settings.KAFKA_CLIENT_ID,
            acks="all",
            retries=3,
            retry_backoff_ms=300,
            linger_ms=5,
            compression_type="gzip",
            max_block_ms=5_000,
        )
        logger.info(
            "Kafka producer ready  servers=%s  client_id=%s",
            servers,
            settings.KAFKA_CLIENT_ID,
        )

    return KafkaEventPublisher(_producer)


def shutdown_event_publisher() -> None:
    """Flush in-flight messages and close the producer on shutdown."""
    global _producer
    if _producer is not None:
        try:
            _producer.flush(timeout=10)
            _producer.close()
            logger.info("Kafka producer flushed and closed")
        except Exception:
            logger.exception("Error while closing Kafka producer")
        finally:
            _producer = None


async def _build_billboard_replication_service() -> BillboardReplicationService:
    db = await get_mongo_database()
    dedup = KafkaEventDeduplicator(db["kafka_processed_events"])
    await dedup.ensure_indexes()
    return BillboardReplicationService(
        MongoCinemaRepository(db),
        MongoTheaterRepository(db),
        MongoShowtimeRepository(db),
        dedup,
    )


def _bootstrap_servers() -> List[str]:
    return [s.strip() for s in settings.KAFKA_BOOTSTRAP_SERVERS.split(",") if s.strip()]


async def _run_billboard_consumer_loop(stop: asyncio.Event) -> None:
    service = await _build_billboard_replication_service()
    servers = _bootstrap_servers()
    if not servers:
        logger.error("Kafka bootstrap servers empty; billboard consumer not started")
        return

    consumer = KafkaConsumer(
        settings.KAFKA_TOPIC_BILLBOARD_EVENTS,
        bootstrap_servers=servers,
        group_id=settings.KAFKA_CONSUMER_GROUP_BILLBOARD,
        client_id=f"{settings.KAFKA_CLIENT_ID}-billboard-consumer",
        enable_auto_commit=False,
        auto_offset_reset=settings.KAFKA_CONSUMER_AUTO_OFFSET_RESET,
        max_poll_records=1,
        value_deserializer=lambda b: b,
    )
    loop = asyncio.get_running_loop()
    poll_ms = settings.KAFKA_CONSUMER_POLL_TIMEOUT_MS

    logger.info(
        "Billboard Kafka consumer subscribed topic=%s group=%s",
        settings.KAFKA_TOPIC_BILLBOARD_EVENTS,
        settings.KAFKA_CONSUMER_GROUP_BILLBOARD,
    )

    try:
        while not stop.is_set():
            records = await loop.run_in_executor(
                None, lambda: consumer.poll(timeout_ms=poll_ms)
            )
            if not records:
                continue
            for _tp, messages in records.items():
                for msg in messages:
                    raw = msg.value
                    try:
                        data = json.loads(raw.decode("utf-8"))
                        if not isinstance(data, dict):
                            raise ValueError("message JSON must be an object")
                        await service.apply_envelope(data)
                        await loop.run_in_executor(None, consumer.commit)
                    except Exception:
                        logger.exception(
                            "failed processing billboard Kafka message offset=%s",
                            getattr(msg, "offset", None),
                        )
    finally:
        await loop.run_in_executor(None, consumer.close)
        logger.info("Billboard Kafka consumer closed")


async def _run_wallet_consumer_loop(stop: asyncio.Event) -> None:
    servers = _bootstrap_servers()
    if not servers:
        logger.error("Kafka bootstrap servers empty; wallet consumer not started")
        return

    consumer = KafkaConsumer(
        settings.KAFKA_WALLET_EVENTS_TOPIC,
        bootstrap_servers=servers,
        group_id=settings.KAFKA_CONSUMER_GROUP_WALLET,
        client_id=f"{settings.KAFKA_CLIENT_ID}-wallet-consumer",
        enable_auto_commit=False,
        auto_offset_reset=settings.KAFKA_CONSUMER_AUTO_OFFSET_RESET,
        max_poll_records=1,
        value_deserializer=lambda b: b,
    )
    loop = asyncio.get_running_loop()
    poll_ms = settings.KAFKA_CONSUMER_POLL_TIMEOUT_MS

    logger.info(
        "Wallet Kafka consumer subscribed topic=%s group=%s",
        settings.KAFKA_WALLET_EVENTS_TOPIC,
        settings.KAFKA_CONSUMER_GROUP_WALLET,
    )

    try:
        while not stop.is_set():
            records = await loop.run_in_executor(
                None, lambda: consumer.poll(timeout_ms=poll_ms)
            )
            if not records:
                continue
            for _tp, messages in records.items():
                for msg in messages:
                    raw = msg.value
                    try:
                        data: Dict[str, Any] = json.loads(raw.decode("utf-8"))
                        if not isinstance(data, dict):
                            raise ValueError("message JSON must be an object")
                        logger.info(
                            "wallet event received event_type=%s event_id=%s",
                            data.get("event_type"),
                            data.get("event_id"),
                        )
                        await loop.run_in_executor(None, consumer.commit)
                    except Exception:
                        logger.exception(
                            "failed parsing wallet Kafka message offset=%s",
                            getattr(msg, "offset", None),
                        )
    finally:
        await loop.run_in_executor(None, consumer.close)
        logger.info("Wallet Kafka consumer closed")


def start_kafka_consumer_tasks(stop: asyncio.Event) -> List[asyncio.Task[None]]:
    """Schedule background consumers; caller must cancel tasks on shutdown."""
    tasks: List[asyncio.Task[None]] = []
    if not settings.KAFKA_CONSUMER_ENABLED:
        return tasks
    if settings.KAFKA_CONSUMER_BILLBOARD_ENABLED:
        tasks.append(asyncio.create_task(_run_billboard_consumer_loop(stop)))
    if settings.KAFKA_CONSUMER_WALLET_ENABLED:
        tasks.append(asyncio.create_task(_run_wallet_consumer_loop(stop)))
    return tasks


