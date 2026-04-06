from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class BaseEvent:
    """
    Base class for all domain events published to Kafka.

    Every subclass must set ``event_type`` as a class-level constant so
    consumers can route by type without deserialising the full payload.
    """

    event_type: str = field(init=False)

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    service: str = "employee-service"
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    correlation_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialise to a plain dict suitable for JSON encoding."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "service": self.service,
            "occurred_at": self.occurred_at.isoformat(),
            "correlation_id": self.correlation_id,
            **self._payload(),
        }

    def _payload(self) -> dict[str, Any]:
        """Override in subclasses to add event-specific fields."""
        return {}
