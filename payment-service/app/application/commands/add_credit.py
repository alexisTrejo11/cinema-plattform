from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.shared.value_objects import PositiveDecimal, TransactionReference, TransactionSource

class AddCreditCommand(BaseModel):
    """Command to add credit to a user's account"""
    user_id: UUID
    amount: PositiveDecimal
    reference_id: TransactionReference
    source: TransactionSource = TransactionSource.SYSTEM
    notes: Optional[str] = Field(None, max_length=500)
    expires_at: Optional[datetime] = None
    idempotency_key: Optional[UUID] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "amount": "50.00",
                "reference_id": "pay_123456",
                "source": "payment",
                "notes": "Credit from PayPal top-up",
                "expires_at": "2024-12-31T23:59:59Z",
                "idempotency_key": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
    }