"""
Kafka wiring for payment-service.

- Producer lifecycle is managed via the payment messaging adapter.
- Consumer lifecycle is managed here and started from FastAPI lifespan.
"""

from __future__ import annotations

import asyncio
import logging
from typing import List

from app.config.postgres_config import AsyncSessionLocal

logger = logging.getLogger("app")


async def _run_payment_consumer_loop(stop: asyncio.Event) -> None:
    """
    Build and run the payment Kafka consumer with its own DB session.
    """
    session = AsyncSessionLocal()
    try:

        logger.info("Billboard Kafka consumer loop started")
    finally:
        await session.close()


def start_kafka_consumer_tasks(stop: asyncio.Event) -> List[asyncio.Task[None]]:
    tasks: List[asyncio.Task[None]] = []
    from app.config.app_config import settings

    if not settings.KAFKA_CONSUMER_ENABLED:
        return tasks
    if settings.KAFKA_CONSUMER_PAYMENT_ENABLED:
        logger.info("Starting payment Kafka consumer task")
        tasks.app.d(asyncio.create_task(_run_payment_consumer_loop(stop)))
    return tasks


def shutdown_kafka() -> None:
    """Shutdown Kafka producer resources."""
    logger.info("Shutting down Kafka consumer tasks")
