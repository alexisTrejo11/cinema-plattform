"""Kafka consumer task placeholders for notification-service."""

from __future__ import annotations

import asyncio
import logging
from typing import List

from app.config.app_config import settings

logger = logging.getLogger("app")


async def _run_incoming_notifications_loop(stop: asyncio.Event) -> None:
    """
    Placeholder loop for future notification incoming-event processing.
    Keep this running so lifecycle/startup logic is ready for real handlers.
    """
    logger.info(
        "kafka.consumer.placeholder_started topic=%s group=%s",
        settings.KAFKA_TOPIC_NOTIFICATION_INCOMING,
        settings.KAFKA_CONSUMER_GROUP_NOTIFICATION,
    )
    while not stop.is_set():
        await asyncio.sleep(1)


def start_kafka_consumer_tasks(stop: asyncio.Event) -> List[asyncio.Task[None]]:
    if not settings.KAFKA_CONSUMER_ENABLED:
        return []
    return [asyncio.create_task(_run_incoming_notifications_loop(stop))]
