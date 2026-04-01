"""
Aggregate root base for domain entities that publish domain events.

Shared logic for ``_events``, ``get_events()``, and ``clear_events()``.
Subclasses may override ``_add_event`` to attach aggregate-specific rules.
"""

from typing import List

from pydantic import BaseModel, ConfigDict, PrivateAttr

from .events import DomainEvent


class AggregateRoot(BaseModel):
    """Base class for aggregates that collect domain events for publishing."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    _events: List[DomainEvent] = PrivateAttr(default_factory=list)

    def get_events(self) -> List[DomainEvent]:
        """Return a copy of pending domain events."""
        return self._events.copy()

    def clear_events(self) -> None:
        """Clear events after they have been published."""
        self._events.clear()

    def _add_event(self, event: DomainEvent) -> None:
        """Append a domain event to this aggregate."""
        self._events.append(event)
