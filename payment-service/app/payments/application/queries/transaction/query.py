from pydantic import BaseModel, Field, UUID4
from typing import Optional

class GetTransactionQuery(BaseModel):
    """Query to get a specific transaction or payment details."""
    transaction_id: Optional[UUID4] = Field(None, description="Transaction ID to lookup.")
    payment_id: Optional[UUID4] = Field(None, description="Payment ID to lookup.")
    wallet_id: Optional[UUID4] = Field(None, description="Wallet ID to get transactions for.")
    user_id: Optional[UUID4] = Field(None, description="User ID to get transactions for.")
    include_payment_details: bool = Field(False, description="Include related payment details.")
    include_wallet_details: bool = Field(False, description="Include wallet information.")

    class Config:
        schema_extra = {
            "example": {
                "transaction_id": "123e4567-e89b-12d3-a456-426614174000",
                "payment_id": "987fcdeb-51a2-43d1-9876-543210fedcba",
                "include_payment_details": True,
                "include_wallet_details": True
            }
        }
