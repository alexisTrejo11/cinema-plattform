from pydantic import BaseModel, Field, UUID4, PositiveFloat
from typing import Optional, Dict, Any
from datetime import datetime


class RefundPaymentCommand(BaseModel):
    payment_id: UUID4 = Field(..., description="ID of the payment to refund.")
    refund_amount: Optional[PositiveFloat] = Field(
        None, description="Amount to refund (full refund if not specified)."
    )
    reason: str = Field(..., max_length=500, description="Reason for the refund.")
    requested_by: UUID4 = Field(
        ..., description="ID of the user/admin requesting the refund."
    )
    refund_to_wallet: bool = Field(
        False, description="Whether to refund to user's wallet."
    )
    correlation_id: Optional[UUID4] = Field(
        None, description="ID for correlating events."
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Timestamp of command creation."
    )

    class Config:
        schema_extra = {
            "example": {
                "payment_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "refund_amount": 75.50,
                "reason": "Customer requested refund due to event cancellation",
                "requested_by": "09876543-21ab-cdef-1234-567890abcdef",
                "refund_to_wallet": True,
            }
        }


class AddCreditCommand(BaseModel):

    user_id: UUID4 = Field(..., description="ID of the user to credit.")
    amount: PositiveFloat = Field(..., gt=0, description="Amount to credit.")
    currency: str = Field(
        "USD", max_length=3, min_length=3, description="Currency code."
    )
    reference_id: str = Field(..., max_length=50, description="External reference ID.")
    source: str = Field("system", description="Source of the credit.")
    description: str = Field(
        ..., max_length=500, description="Description of the credit."
    )
    wallet_id: Optional[UUID4] = Field(
        None, description="Specific wallet ID (optional)."
    )
    expires_at: Optional[datetime] = Field(None, description="Credit expiration date.")
    idempotency_key: Optional[UUID4] = Field(None, description="Idempotency key.")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Timestamp of command creation."
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "amount": 50.00,
                "currency": "USD",
                "reference_id": "pay_123456",
                "source": "payment",
                "description": "Credit from PayPal top-up",
                "expires_at": "2024-12-31T23:59:59Z",
                "idempotency_key": "550e8400-e29b-41d4-a716-446655440000",
            }
        }
    }


class ProcessPayCommand(BaseModel):
    """
    Command to initiate payment processing.
    """

    product_id: UUID4 = Field(..., description="Unique ID of the product to purchase.")
    user_id: UUID4 = Field(..., description="ID of the user making the purchase.")
    amount: PositiveFloat = Field(..., gt=0, description="Total purchase amount.")
    payment_method: str = Field(
        ...,
        pattern="^(wallet|credit_card|debit_card|paypal|stripe)$",
        description="Payment method.",
    )
    payment_type: str = Field(
        ...,
        pattern="^(ticket_purchase|food_purchase|merchandise_purchase|wallet_topup)$",
        description="Type of payment.",
    )
    wallet_id: Optional[UUID4] = Field(
        None, description="Wallet ID if payment method is 'wallet'."
    )
    currency: str = Field(
        "USD",
        max_length=3,
        min_length=3,
        description="Currency code (e.g., 'MXN', 'USD').",
    )
    correlation_id: Optional[UUID4] = Field(
        None, description="ID for correlating events."
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Additional payment metadata."
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Timestamp of command creation."
    )

    class Config:
        schema_extra = {
            "example": {
                "product_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "user_id": "09876543-21ab-cdef-1234-567890abcdef",
                "amount": 150.75,
                "payment_method": "wallet",
                "payment_type": "ticket_purchase",
                "wallet_id": "fedcba98-7654-3210-fedc-ba9876543210",
                "currency": "USD",
            }
        }
