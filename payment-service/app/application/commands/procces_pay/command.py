from pydantic import BaseModel, Field, PositiveFloat, UUID4
from typing import Optional, Dict, Any
from datetime import datetime

class ProcessPayCommand(BaseModel):
    """
    Command to initiate payment processing.
    """
    product_id: UUID4 = Field(..., description="Unique ID of the product to purchase.")
    user_id: UUID4 = Field(..., description="ID of the user making the purchase.")
    amount: PositiveFloat = Field(..., gt=0, description="Total purchase amount.")
    payment_method: str = Field(..., pattern="^(wallet|credit_card|debit_card|paypal|stripe)$", description="Payment method.")
    payment_type: str = Field(..., pattern="^(ticket_purchase|food_purchase|merchandise_purchase|wallet_topup)$", description="Type of payment.")
    wallet_id: Optional[UUID4] = Field(None, description="Wallet ID if payment method is 'wallet'.")
    currency: str = Field("USD", max_length=3, min_length=3, description="Currency code (e.g., 'MXN', 'USD').")
    correlation_id: Optional[UUID4] = Field(None, description="ID for correlating events.")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional payment metadata.")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of command creation.")

    class Config:
        schema_extra = {
            "example": {
                "product_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "user_id": "09876543-21ab-cdef-1234-567890abcdef",
                "amount": 150.75,
                "payment_method": "wallet",
                "payment_type": "ticket_purchase",
                "wallet_id": "fedcba98-7654-3210-fedc-ba9876543210",
                "currency": "USD"
            }
        }
