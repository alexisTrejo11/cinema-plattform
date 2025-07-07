from pydantic import BaseModel, Field, PositiveFloat, UUID4
from typing import Optional
from datetime import datetime
from uuid import UUID

class ProcessPayCommand(BaseModel):
    """
    Command to initiate payment processing.
    """
    product_id: UUID4 = Field(..., description="Unique ID of the product to purchase.")
    user_id: UUID4 = Field(..., description="ID of the user making the purchase.")
    amount: PositiveFloat = Field(..., gt=0, description="Total purchase amount.")
    payment_method: str = Field(..., pattern="^(wallet|credit_card|debit_card)$", description="Payment method.")
    wallet_id: Optional[UUID4] = Field(None, description="Wallet ID if payment method is 'wallet'.")
    currency: str = Field("MXN", max_length=3, min_length=3, description="Currency code (e.g., 'MXN', 'USD').")
    correlation_id: Optional[UUID4] = Field(None, description="ID for correlating events.")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of command creation.")

    class Config:
        schema_extra = {
            "example": {
                "product_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "user_id": "09876543-21ab-cdef-1234-567890abcdef",
                "amount": 150.75,
                "payment_method": "wallet",
                "wallet_id": "fedcba98-7654-3210-fedc-ba9876543210",
                "currency": "MXN"
            }
        }