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
    Kafka when ``KAFKA_ENABLED`` and bootstrap servers are set; otherwise no-op.
    """
    global _producer
    if not settings.KAFKA_ENABLED or not settings.KAFKA_BOOTSTRAP_SERVERS.strip():
        logger.info("Kafka event publisher disabled (noop)")
        return NoopEventPublisher()

    if _producer is None:
        servers = [s.strip() for s in settings.KAFKA_BOOTSTRAP_SERVERS.split(",") if s.strip()]
        _producer = KafkaProducer(
            bootstrap_servers=servers,
            client_id=settings.KAFKA_CLIENT_ID,
            acks="all",
            retries=3,
            linger_ms=5,
        )
        logger.info(
            "Kafka producer ready topic=%s",
            settings.KAFKA_USER_EVENTS_TOPIC,
        )

    return KafkaEventPublisher(_producer, topic=settings.KAFKA_USER_EVENTS_TOPIC)


def shutdown_event_publisher() -> None:
    """Flush and close producer on application shutdown."""
    global _producer
    if _producer is not None:
        try:
            _producer.flush(timeout=10)
            _producer.close()
        except Exception:
            logger.exception("Error while closing Kafka producer")
        finally:
            _producer = None
            logger.info("Kafka producer closed")
