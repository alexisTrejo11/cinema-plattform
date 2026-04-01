import uuid
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from ..value_objects import PaymentProvider, PaymentMethodType


class PaymentMethod(BaseModel):
    """
    Entity of the Payment Method Catalog.
    Defines the payment options available in the system (Cinema).
    """

    model_config = ConfigDict(
        frozen=True, validate_assignment=True, from_attributes=True
    )

    id: str = Field(..., description="Unique ID (e.g. stripe-card-mx)")
    name: str = Field(..., description="Commercial name (e.g. Credit Card)")

    provider: PaymentProvider
    type: PaymentMethodType

    stripe_code: str = Field(
        ..., description="The code that Stripe understands (e.g. 'card', 'oxxo')"
    )

    is_active: bool = True

    min_amount: float = Field(default=0.0, ge=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = None

    @field_validator("id")
    @classmethod
    def id_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("ID cannot be empty")
        return v.lower()

    def can_process_amount(self, amount: float) -> bool:
        """Check if the amount meets the minimum of the method."""
        return self.is_active and amount >= self.min_amount

    def is_stripe_card(self) -> bool:
        """Helper for specific Stripe Cards logic."""
        return (
            self.provider == PaymentProvider.STRIPE
            and self.type == PaymentMethodType.CARD
        )

    def is_cash_payment(self) -> bool:
        """Check if the payment requires asynchronous confirmation (webhook)."""
        return self.type == PaymentMethodType.CASH

    def mark_as_inactive(self) -> "PaymentMethod":
        """Return a copy of the deactivated method (Immutability)."""
        return self.model_copy(
            update={"is_active": False, "updated_at": datetime.now(timezone.utc)}
        )

    def mark_as_deleted(self) -> "PaymentMethod":
        """Return a copy of the deleted method (Immutability)."""
        return self.model_copy(update={"deleted_at": datetime.now(timezone.utc)})

    def mark_as_active(self) -> "PaymentMethod":
        """Clear soft-delete and ensure the catalog entry is active again."""
        return self.model_copy(
            update={
                "is_active": True,
                "deleted_at": None,
                "updated_at": datetime.now(timezone.utc),
            }
        )

    @classmethod
    def create(cls, **kwargs) -> "PaymentMethod":
        """
        Create a new payment method.
        Generates a new UUID for the ID and sets timestamps.
        """
        id = uuid.uuid4()
        created_at = datetime.now(timezone.utc)
        updated_at = created_at

        return cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            **kwargs,
        )

    def update(self, update_data: dict) -> "PaymentMethod":
        """
        Update (partially) the payment method.
        Recieves a dictionary of the fields to update.
        Sets the updated_at timestamp and resets the deleted_at timestamp.
        """
        now = datetime.now(timezone.utc)
        return self.model_copy(
            update={**update_data, "updated_at": now, "deleted_at": None}
        )
