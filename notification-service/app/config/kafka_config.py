"""Kafka incoming-consumer tasks for notification-service."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
import json
import logging
from typing import List
from uuid import uuid4

from kafka import KafkaConsumer

from app.config.app_config import settings
from app.config.mongo_config import get_mongo_database
from app.notification.application.commands.notification_command import (
    ProcessIncomingNotificationEventCommand,
)
from app.notification.application.usecases.incoming_event_usecases import (
    ProcessIncomingNotificationEventUseCase,
)
from app.notification.infrastructure.email.mail_service import EmailService
from app.notification.infrastructure.external.user_profile_http_service import (
    HttpUserProfileService,
)
from app.notification.infrastructure.message.sms_message_services import SmsMessageService
from app.notification.infrastructure.repository.mongo_notification_repository import (
    MongoNotificationRepository,
)
from app.notification.infrastructure.services import SendingServiceImplementation

logger = logging.getLogger("app")


def _parse_topics() -> list[str]:
    return [topic.strip() for topic in settings.KAFKA_CONSUMER_TOPICS.split(",") if topic.strip()]


def _build_usecase(database) -> ProcessIncomingNotificationEventUseCase:
    repository = MongoNotificationRepository(database)
    sender = SendingServiceImplementation(
        email_service=EmailService(),
        sms_service=SmsMessageService(),
    )
    user_profile_service = HttpUserProfileService()
    return ProcessIncomingNotificationEventUseCase(
        repository=repository,
        sending_service=sender,
        user_profile_service=user_profile_service,
    )


def _extract_command(raw_value: dict, *, topic: str, partition: int, offset: int) -> ProcessIncomingNotificationEventCommand:
    payload = dict(raw_value or {})

    event_type = payload.get("event_type")
    nested_data = payload.get("data") if isinstance(payload.get("data"), dict) else None
    event_payload = payload.get("payload")
    if not isinstance(event_payload, dict):
        event_payload = nested_data or payload
    if not event_type and isinstance(nested_data, dict):
        event_type = nested_data.get("event_type")
    if not event_type:
        event_type = "notification.unknown"

    event_id = payload.get("event_id")
    if not event_id:
        event_id = f"{topic}-{partition}-{offset}-{uuid4()}"

    occurred_at_raw = payload.get("occurred_at")
    occurred_at = datetime.now(timezone.utc)
    if isinstance(occurred_at_raw, str):
        try:
            occurred_at = datetime.fromisoformat(occurred_at_raw.replace("Z", "+00:00"))
        except ValueError:
            pass

    return ProcessIncomingNotificationEventCommand(
        event_type=str(event_type),
        event_id=str(event_id),
        payload=event_payload,
        source=str(payload.get("source", topic)),
        occurred_at=occurred_at,
        correlation_id=(
            str(payload.get("correlation_id"))
            if payload.get("correlation_id") is not None
            else None
        ),
    )


async def _run_incoming_notifications_loop(stop: asyncio.Event) -> None:
    topics = _parse_topics()
    bootstrap_servers = [
        server.strip()
        for server in settings.KAFKA_BOOTSTRAP_SERVERS.split(",")
        if server.strip()
    ]
    if not topics:
        logger.warning("kafka.consumer.no_topics_configured")
        return
    if not bootstrap_servers:
        logger.warning("kafka.consumer.no_bootstrap_servers")
        return

    logger.info(
        "kafka.consumer.started topics=%s group=%s bootstrap=%s",
        ",".join(topics),
        settings.KAFKA_CONSUMER_GROUP_NOTIFICATION,
        settings.KAFKA_BOOTSTRAP_SERVERS,
    )

    database = await get_mongo_database()
    usecase = _build_usecase(database)
    consumer = KafkaConsumer(
        *topics,
        bootstrap_servers=bootstrap_servers,
        client_id=f"{settings.KAFKA_CLIENT_ID}-incoming",
        group_id=settings.KAFKA_CONSUMER_GROUP_NOTIFICATION,
        auto_offset_reset=settings.KAFKA_CONSUMER_AUTO_OFFSET_RESET,
        enable_auto_commit=True,
    )
    try:
        while not stop.is_set():
            records = await asyncio.to_thread(
                consumer.poll,
                timeout_ms=settings.KAFKA_CONSUMER_POLL_TIMEOUT_MS,
                max_records=100,
            )
            if not records:
                continue

            for topic_partition, messages in records.items():
                for msg in messages:
                    try:
                        raw_value = msg.value
                        if isinstance(raw_value, (bytes, bytearray)):
                            raw_value = json.loads(raw_value.decode("utf-8"))
                        if not isinstance(raw_value, dict):
                            logger.warning(
                                "kafka.consumer.unsupported_payload topic=%s partition=%s offset=%s",
                                topic_partition.topic,
                                topic_partition.partition,
                                msg.offset,
                            )
                            continue
                        command = _extract_command(
                            raw_value,
                            topic=topic_partition.topic,
                            partition=topic_partition.partition,
                            offset=msg.offset,
                        )
                        await usecase.execute(command)
                    except Exception:
                        logger.exception(
                            "kafka.consumer.message_failed topic=%s partition=%s offset=%s",
                            topic_partition.topic,
                            topic_partition.partition,
                            msg.offset,
                        )
    finally:
        await asyncio.to_thread(consumer.close)
        logger.info("kafka.consumer.stopped")


def start_kafka_consumer_tasks(stop: asyncio.Event) -> List[asyncio.Task[None]]:
    if not settings.KAFKA_CONSUMER_ENABLED:
        return []
    return [asyncio.create_task(_run_incoming_notifications_loop(stop))]
