from __future__ import annotations

import logging
from typing import Optional

from kafka import KafkaProducer

from app.config.app_config import settings
from app.shared.events.infrastructure.kafka_publisher import KafkaEventPublisher
from app.shared.events.infrastructure.noop_publisher import NoopEventPublisher
from app.shared.events.protocols import EventPublisher

logger = logging.getLogger(__name__)

_producer: Optional[KafkaProducer] = None


def create_event_publisher() -> EventPublisher:
    """
    Returns a KafkaEventPublisher when Kafka is configured,
    or a NoopEventPublisher for local / test environments.
    Called once at application startup and stored on app.state.
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
