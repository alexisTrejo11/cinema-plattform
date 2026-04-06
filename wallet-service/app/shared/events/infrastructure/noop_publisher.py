from __future__ import annotations

import logging

from app.shared.events.base import BaseEvent

logger = logging.getLogger(__name__)


class NoopEventPublisher:
    """
    No-op publisher used when Kafka is disabled (development / testing).
    Logs at DEBUG level so events are still visible in logs.
    """

    def publish(self, topic: str, event: BaseEvent) -> None:
        logger.debug(
            "[noop] Event not published  type=%s  topic=%s  event_id=%s",
            event.event_type,
            topic,
            event.event_id,
        )
