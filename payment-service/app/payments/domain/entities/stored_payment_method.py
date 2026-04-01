"""
Saved payment method aggregate (user card / token metadata).

Distinct from the ``PaymentMethod`` enum in ``value_objects`` (payment rail type).
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from pydantic import ConfigDict

from app.payments.domain.value_objects import Card, UserId
from ..aggregate_root import AggregateRoot
from ..events import DomainEvent, PaymentMethodAdded, PaymentMethodRemoved


class StoredPaymentMethod(AggregateRoot):
    """
    A persisted payment method for a user (e.g. tokenized card).

    ``Card.stripe_payment_method_id`` holds the Stripe ``pm_xxx`` when using Stripe.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str
    user_id: str
    payment_method_id: str
    provider_token: str
    card: Optional[Card]
    is_default: bool = False
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    def _add_event(self, event: DomainEvent) -> None:
        agg = UUID(self.id)
        if event.aggregate_id != agg:
            event = event.model_copy(update={"aggregate_id": agg})
        self._events.append(event)

    @classmethod
    def create(
        cls,
        user_id: str,
        card: Card,
        *,
        is_default: bool = False,
    ) -> "StoredPaymentMethod":
        """Create a new saved payment method and emit ``PaymentMethodAdded``."""
        now = datetime.now(timezone.utc)
        sid = str(uuid4())
        token = card.stripe_payment_method_id or ""
        entity = cls(
            id=sid,
            user_id=user_id,
            payment_method_id=token or "card",
            provider_token=token,
            card=card,
            is_default=is_default,
            created_at=now,
            updated_at=now,
            deleted_at=None,
        )
        entity._add_event(
            PaymentMethodAdded(
                payment_method_id=sid,
                user_id=UserId.from_string(user_id),
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
                payment_method_id=self.id,
                user_id=UserId.from_string(self.user_id),
            )
        )
