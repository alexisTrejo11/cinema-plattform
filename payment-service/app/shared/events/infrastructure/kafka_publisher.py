from __future__ import annotations

import json
import logging

from kafka import KafkaProducer

from app.shared.events.base import IntegrationEvent

logger = logging.getLogger(__name__)


class KafkaEventPublisher:
    """
    Adapter: publishes domain events to Kafka topics as UTF-8 JSON.

    Uses kafka-python's async-buffered producer — `send()` is non-blocking;
    the internal sender thread handles network I/O and retries.
    """

    def __init__(self, producer: KafkaProducer) -> None:
        self._producer = producer

    def publish(self, topic: str, event: IntegrationEvent) -> None:
        try:
            payload = json.dumps(event.to_dict(), default=str).encode("utf-8")
            key = str(event.event_id).encode("utf-8")
            self._producer.send(topic=topic, value=payload, key=key)
            logger.debug(
                "Event queued  type=%s  topic=%s  event_id=%s",
                event.event_type(),
                topic,
                event.event_id,
            )
        except Exception:
            # Publishing must never crash the write path.
            logger.exception(
                "Failed to enqueue event type=%s topic=%s", event.event_type(), topic
            )
