from typing import Protocol

from app.shared.events.envelope import DomainEventEnvelope


class EventPublisher(Protocol):
    """Outbound integration port — implemented by Kafka (or no-op for local/tests)."""

    async def publish(self, envelope: DomainEventEnvelope) -> None:
        ...
