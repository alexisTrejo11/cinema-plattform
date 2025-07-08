from pydantic import BaseModel, Field, PositiveFloat, UUID4
from datetime import datetime
from typing import Optional

class AddCreditCommand(BaseModel):
    """Command to add credit to a user's account"""
    user_id: UUID4 = Field(..., description="ID of the user to credit.")
    amount: PositiveFloat = Field(..., gt=0, description="Amount to credit.")
    currency: str = Field("USD", max_length=3, min_length=3, description="Currency code.")
    reference_id: str = Field(..., max_length=50, description="External reference ID.")
    source: str = Field("system", description="Source of the credit.")
    description: str = Field(..., max_length=500, description="Description of the credit.")
    wallet_id: Optional[UUID4] = Field(None, description="Specific wallet ID (optional).")
    expires_at: Optional[datetime] = Field(None, description="Credit expiration date.")
    idempotency_key: Optional[UUID4] = Field(None, description="Idempotency key.")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of command creation.")

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
                "idempotency_key": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
    }



