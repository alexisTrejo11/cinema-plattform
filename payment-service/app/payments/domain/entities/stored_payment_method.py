"""
Saved payment method aggregate (user card / token metadata).

Distinct from the ``PaymentMethod`` enum in ``value_objects`` (payment rail type).
"""

from datetime import datetime, timezone
from typing import Optional

from pydantic import ConfigDict

from ..aggregate_root import AggregateRoot
from ..events import DomainEvent, PaymentMethodAdded, PaymentMethodRemoved
from ..value_objects import ID, Card, UserId

from enum import Enum


class StoredPaymentMethod(AggregateRoot):
    """
    A persisted payment method for a user (e.g. tokenized card).

    ``Card.stripe_payment_method_id`` holds the Stripe ``pm_xxx`` when using Stripe.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ID
    user_id: UserId
    payment_method_id: str

    provider_token: str
    card: Optional[Card]
    is_default: bool = False
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    def _add_event(self, event: DomainEvent) -> None:
        if event.aggregate_id != self.id.value:
            event = event.model_copy(update={"aggregate_id": self.id.value})
        self._events.append(event)

    @classmethod
    def create(
        cls,
        user_id: UserId,
        card: Card,
        *,
        is_default: bool = False,
    ) -> StoredPaymentMethod:
        """Create a new saved payment method and emit ``PaymentMethodAdded``."""
        now = datetime.now(timezone.utc)
        pm_id = ID.generate()
        entity = cls(
            id=pm_id,
            user_id=user_id,
            card=card,
            is_default=is_default,
            created_at=now,
            updated_at=now,
            deleted_at=None,
        )
        entity._add_event(
            PaymentMethodAdded(
                payment_method_id=str(pm_id.value),
                user_id=user_id,
            )
        )
        return entity

    def is_active(self) -> bool:
        """Whether this payment method is not soft-deleted."""
        return self.deleted_at is None

    def delete(self) -> None:
        """Soft-delete this payment method and emit ``PaymentMethodRemoved``."""
        if self.deleted_at is not None:
            return
        now = datetime.now(timezone.utc)
        self.deleted_at = now
        self.updated_at = now
        self._add_event(
            PaymentMethodRemoved(
                payment_method_id=str(self.id.value),
                user_id=self.user_id,
            )
        )
