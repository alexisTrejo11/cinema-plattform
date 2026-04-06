from typing import Any, Protocol, runtime_checkable, Dict, Optional
from abc import ABC, abstractmethod
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field


@runtime_checkable
class IntegrationEvent(Protocol):
    """
    Contract for events that can be serialized and published (Kafka, outbox).

    Payment :class:`~app.ayments.domain.events.DomainEvent` subclasses implement
    this structurally — use that as the concrete base; this Protocol is only for
    typing generic publishers and static checks.

    Do not add a second parallel event hierarchy; extend ``DomainEvent`` instead.
    """

    event_id: UUID

    def event_type(self) -> str:
        """Stable routing key, e.g. ``payment.completed``."""

    def to_dict(self) -> dict[str, Any]:
        """JSON-friendly envelope (see payment ``DomainEvent.to_dict``)."""


# Backward-compatible alias (was a dataclass; now the Protocol above).
BaseEvent = IntegrationEvent


class DomainEvent(BaseModel, ABC):
    """Base class for all payment domain events (implements ``IntegrationEvent`` for outbox/Kafka)."""

    model_config = ConfigDict(frozen=True)

    event_id: UUID = Field(default_factory=uuid4)
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    aggregate_id: Optional[UUID] = None
    version: int = 1

    @abstractmethod
    def event_type(self) -> str:
        """Stable integration name, e.g. ``payment.completed``."""

    @abstractmethod
    def _get_event_data(self) -> Dict[str, Any]:
        """Payload merged under ``data`` in :meth:`to_dict`."""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type(),
            "occurred_at": self.occurred_at.isoformat(),
            "aggregate_id": str(self.aggregate_id) if self.aggregate_id else None,
            "version": self.version,
            "data": self._get_event_data(),
        }
