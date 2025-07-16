from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime
from app.wallet.domain.value_objects import Money, PaymentDetails, Currency
from app.wallet.domain.entities.wallet import Wallet, WalletTransaction

class WalletOperationRequest(BaseModel):
    """
    DTO for requesting a credit addition or other specific operations to a wallet.
    This model defines the necessary input parameters for such operations.
    """
    wallet_id: UUID = Field(
        ...,
        description="The unique identifier of the target wallet for the operation.",
        json_schema_extra={"example": "a1b2c3d4-e5f6-7890-1234-567890abcdef"}
    )
    amount: Decimal = Field(
        ...,
        description="The amount of money involved in the operation. Must be a positive decimal number.",
        gt=0, # Ensures the amount is greater than zero
        json_schema_extra={"example": 150.75}
    )
    currency: Currency = Field(
        ...,
        description="The currency of the amount (e.g., USD, MXN, EUR).",
        json_schema_extra={"example": "USD"} # Example assumes Currency is an Enum of strings
    )
    payment_id: UUID = Field(
        ...,
        description="A unique identifier for the associated payment or external transaction.",
        json_schema_extra={"example": "b2c3d4e5-f6a7-8901-2345-67890abcdef1"}
    )
    payment_method: str = Field(
        ...,
        description="The method used for the payment (e.g., 'card', 'bank_transfer', 'crypto').",
        json_schema_extra={"example": "card"}
    )

    model_config = ConfigDict(from_attributes=True)
    model_config["json_schema_extra"] = {
        "example": {
            "wallet_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
            "amount": 150.75,
            "currency": "USD",
            "payment_id": "b2c3d4e5-f6a7-8901-2345-67890abcdef1",
            "payment_method": "card"
        }
    }