import logging

from app.shared.events.envelope import DomainEventEnvelope
from app.shared.events.protocols import EventPublisher

logger = logging.getLogger(__name__)


class NoopEventPublisher:
    """Used when Kafka is disabled; keeps application logic testable without a broker."""

    async def publish(self, envelope: DomainEventEnvelope) -> None:
        logger.debug(
            "event not published (noop) type=%s id=%s",
            envelope.event_type.value,
            envelope.event_id,
        )
