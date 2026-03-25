from __future__ import annotations

import asyncio
import logging
from typing import Optional

from kafka import KafkaProducer

from app.shared.events.envelope import DomainEventEnvelope
from app.shared.events.protocols import EventPublisher

logger = logging.getLogger(__name__)


class KafkaEventPublisher(EventPublisher):
    """
    Publishes ``DomainEventEnvelope`` JSON to a single topic; consumers route on ``event_type``.
    """

    def __init__(
        self,
        producer: KafkaProducer,
        topic: str,
    ) -> None:
        self._producer = producer
        self._topic = topic

    async def publish(self, envelope: DomainEventEnvelope) -> None:
        data = envelope.model_dump_json().encode("utf-8")
        key = self._partition_key(envelope)
        await asyncio.to_thread(self._send_sync, data, key)

    def _partition_key(self, envelope: DomainEventEnvelope) -> Optional[bytes]:
        uid = envelope.payload.get("user_id")
        if uid is not None:
            return str(uid).encode("utf-8")
        return envelope.event_id.encode("utf-8")

    def _send_sync(self, data: bytes, key: Optional[bytes]) -> None:
        try:
            future = self._producer.send(self._topic, key=key, value=data)
            future.get(timeout=10)
        except Exception:
            logger.exception("failed to publish kafka event topic=%s", self._topic)
            raise
