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
from app.payments.application.services.payment_incoming_events_handler import (
    PaymentIncomingEventsHandler,
)
from app.payments.infrastructure.messaging.kafka_payment_events import (
    PaymentInboundKafkaConsumer,
    close_kafka_producer,
)
from app.payments.infrastructure.persistence.sql_alchemy_repository import (
    SqlAlchemyPaymentRepository,
)
from app.payments.presentation.depencies import get_payment_events_publisher

logger = logging.getLogger(__name__)


async def _run_payment_consumer_loop(stop: asyncio.Event) -> None:
    """
    Build and run the payment Kafka consumer with its own DB session.
    """
    session = AsyncSessionLocal()
    try:
        payment_repo = SqlAlchemyPaymentRepository(session)
        publisher = get_payment_events_publisher()
        handler = PaymentIncomingEventsHandler(payment_repo, publisher)
        consumer = PaymentInboundKafkaConsumer(handler)
        await consumer.run(stop)
    finally:
        await session.close()


def start_kafka_consumer_tasks(stop: asyncio.Event) -> List[asyncio.Task[None]]:
    tasks: List[asyncio.Task[None]] = []
    from app.config.app_config import settings

    if not settings.KAFKA_CONSUMER_ENABLED:
        return tasks
    if settings.KAFKA_CONSUMER_PAYMENT_ENABLED:
        logger.info("Starting payment Kafka consumer task")
        tasks.append(asyncio.create_task(_run_payment_consumer_loop(stop)))
    return tasks


def shutdown_kafka() -> None:
    """Shutdown Kafka producer resources."""
    close_kafka_producer()
