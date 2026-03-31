from __future__ import annotations

from typing import Protocol, runtime_checkable

from .base import BaseEvent


@runtime_checkable
class EventPublisher(Protocol):
    """
    Port: anything that can publish a domain event to a topic.

    Implementations: KafkaEventPublisher, NoopEventPublisher.
    The call is intentionally synchronous — kafka-python's producer.send()
    buffers internally and never blocks the caller.
    """

    def publish(self, topic: str, event: BaseEvent) -> None:
        """Publish *event* to *topic*. Must never raise."""
        ...
