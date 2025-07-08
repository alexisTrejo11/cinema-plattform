from pydantic import BaseModel, Field, PositiveFloat, UUID4
from typing import Optional
from datetime import datetime

class RefundPaymentCommand(BaseModel):
    """
    Command to refund a payment.
    """
    payment_id: UUID4 = Field(..., description="ID of the payment to refund.")
    refund_amount: Optional[PositiveFloat] = Field(None, description="Amount to refund (full refund if not specified).")
    reason: str = Field(..., max_length=500, description="Reason for the refund.")
    requested_by: UUID4 = Field(..., description="ID of the user/admin requesting the refund.")
    refund_to_wallet: bool = Field(False, description="Whether to refund to user's wallet.")
    correlation_id: Optional[UUID4] = Field(None, description="ID for correlating events.")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of command creation.")

    class Config:
        schema_extra = {
            "example": {
                "payment_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "refund_amount": 75.50,
                "reason": "Customer requested refund due to event cancellation",
                "requested_by": "09876543-21ab-cdef-1234-567890abcdef",
                "refund_to_wallet": True
            }
        }