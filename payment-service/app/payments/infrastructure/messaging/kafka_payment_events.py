from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Optional

from kafka import KafkaConsumer, KafkaProducer

from app.config.app_config import settings
from app.payments.domain.interfaces import PaymentEventsPublisher

logger = logging.getLogger(__name__)

_producer: Optional[KafkaProducer] = None


def _bootstrap_servers() -> list[str]:
    return [s.strip() for s in settings.KAFKA_BOOTSTRAP_SERVERS.split(",") if s.strip()]


class KafkaPaymentEventsPublisher(PaymentEventsPublisher):
    """
    Kafka adapter for publishing payment integration events.

    This class intentionally keeps a small API aligned with the domain port.
    """

    def __init__(self, producer: KafkaProducer, topic: str) -> None:
        self._producer = producer
        self._topic = topic

    async def publish(
        self, event_name: str, payload: dict[str, Any], key: str | None = None
    ) -> None:
        try:
            message = {
                "event_type": event_name,
                "service": settings.SERVICE_NAME,
                "payload": payload,
            }
            value = json.dumps(message, default=str).encode("utf-8")
            kafka_key = key.encode("utf-8") if key else None
            self._producer.send(topic=self._topic, key=kafka_key, value=value)
        except Exception:
            # Keep write paths resilient; failure is logged for later retries/alerts.
            logger.exception("failed to publish payment event event_type=%s", event_name)


class NoopPaymentEventsPublisher(PaymentEventsPublisher):
    async def publish(
        self, event_name: str, payload: dict[str, Any], key: str | None = None
    ) -> None:
        logger.debug(
            "[noop] payment event skipped event_type=%s key=%s payload=%s",
            event_name,
            key,
            payload,
        )


def get_or_create_kafka_producer() -> Optional[KafkaProducer]:
    global _producer
    if not settings.KAFKA_ENABLED:
        return None
    servers = _bootstrap_servers()
    if not servers:
        logger.warning("Kafka enabled but no bootstrap servers configured")
        return None
    if _producer is None:
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
            "Kafka payment producer ready servers=%s topic=%s",
            servers,
            settings.KAFKA_TOPIC_PAYMENT_EVENTS,
        )
    return _producer


def close_kafka_producer() -> None:
    global _producer
    if _producer is None:
        return
    try:
        _producer.flush(timeout=10)
        _producer.close()
        logger.info("Kafka payment producer flushed and closed")
    except Exception:
        logger.exception("failed closing Kafka producer")
    finally:
        _producer = None


def build_payment_events_publisher() -> PaymentEventsPublisher:
    producer = get_or_create_kafka_producer()
    if producer is None:
        return NoopPaymentEventsPublisher()
    return KafkaPaymentEventsPublisher(producer, topic=settings.KAFKA_TOPIC_PAYMENT_EVENTS)


class PaymentInboundKafkaConsumer:
    """
    Minimal inbound Kafka consumer for payment-service integration events.

    The handler receives normalized dict payloads. It may update local payment state
    and publish follow-up events.
    """

    def __init__(self, handler: "PaymentIncomingEventsHandler") -> None:
        self._handler = handler

    async def run(self, stop: asyncio.Event) -> None:
        if not settings.KAFKA_CONSUMER_ENABLED or not settings.KAFKA_CONSUMER_PAYMENT_ENABLED:
            return

        servers = _bootstrap_servers()
        if not servers:
            logger.error("Kafka bootstrap servers empty; payment consumer not started")
            return

        consumer = KafkaConsumer(
            settings.KAFKA_TOPIC_PAYMENT_INCOMING,
            bootstrap_servers=servers,
            group_id=settings.KAFKA_CONSUMER_GROUP_PAYMENT,
            client_id=f"{settings.KAFKA_CLIENT_ID}-payment-consumer",
            enable_auto_commit=False,
            auto_offset_reset=settings.KAFKA_CONSUMER_AUTO_OFFSET_RESET,
            max_poll_records=10,
            value_deserializer=lambda b: b,
        )
        loop = asyncio.get_running_loop()
        poll_ms = settings.KAFKA_CONSUMER_POLL_TIMEOUT_MS
        logger.info(
            "Payment Kafka consumer subscribed topic=%s group=%s",
            settings.KAFKA_TOPIC_PAYMENT_INCOMING,
            settings.KAFKA_CONSUMER_GROUP_PAYMENT,
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
                        try:
                            data = json.loads(msg.value.decode("utf-8"))
                            if not isinstance(data, dict):
                                raise ValueError("message JSON must be an object")
                            await self._handler.handle(data)
                            await loop.run_in_executor(None, consumer.commit)
                        except Exception:
                            logger.exception(
                                "failed processing payment Kafka message offset=%s",
                                getattr(msg, "offset", None),
                            )
        finally:
            await loop.run_in_executor(None, consumer.close)
            logger.info("Payment Kafka consumer closed")


# Local import to avoid circular dependencies during module initialization.
from app.payments.application.services.payment_incoming_events_handler import (  # noqa: E402
    PaymentIncomingEventsHandler,
)
