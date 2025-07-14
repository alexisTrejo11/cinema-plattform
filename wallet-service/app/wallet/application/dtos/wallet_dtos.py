from pydantic import BaseModel, Field
from uuid import UUID
from app.user.domain.value_objects import UserId
from app.user.application.dtos import PydanticUserId
from app.wallet.domain.value_objects import Money, PaymentDetails
from app.wallet.domain.enums import TransactionType
from decimal import Decimal


class WalletResponse(BaseModel):
    """DTO for wallet information."""

    id: UUID
    user_id: UUID
    balance: Decimal


# Create Response for transaction
class BuyCreditResponse(WalletResponse):
    """DTO for wallet information."""

    transaction: dict

    class Config:
        orm_mode = True


class WalletBuyResponse(WalletResponse):
    """DTO for wallet information."""

    transaction: dict

    class Config:
        orm_mode = True


class CreateWalletResponse(BaseModel):
    """DTO for creating a new wallet."""

    user_id: PydanticUserId = Field(
        ..., description="The ID of the user who will own the new wallet."
    )


class CreateWalletCommand(BaseModel):
    """DTO for creating a new wallet."""

    user_id: PydanticUserId = Field(
        ..., description="The ID of the user who will own the new wallet."
    )


class AddCreditRequest(BaseModel):
    """DTO for adding credit to a wallet."""

    wallet_id: UUID = Field(..., description="The ID of the wallet to add credit to.")
    amount: float = Field(
        ..., gt=0, description="The amount of credit to add. Must be a positive number."
    )
    currency: str = Field(..., description="MXN OR USD")


class AddCreditCommand(BaseModel):
    """DTO for adding credit to a wallet."""

    wallet_id: UUID = Field(..., description="The ID of the wallet to add credit to.")
    transaction_type: TransactionType = Field(
        ..., description="The type of transaction (e.g., CREDIT)."
    )
    payment_details: PaymentDetails = Field(
        ..., description="Payment details for the transaction."
    )
    amount: Money = Field(
        ..., gt=0, description="The amount of credit to add. Must be a positive number."
    )


class PayResponse(BaseModel):
    """DTO for making a payment from a wallet."""

    wallet_id: UUID = Field(..., description="The ID of the wallet to pay from.")
    amount: float = Field(
        ..., gt=0, description="The amount to pay. Must be a positive number."
    )


class PayWithWalletCommand(BaseModel):
    """DTO for making a payment from a wallet."""

    wallet_id: UUID = Field(..., description="The ID of the wallet to pay from.")
    payment_details: PaymentDetails = Field(
        ..., description="Payment details for the transaction."
    )
    amount: Money = Field(
        ..., gt=0, description="The amount of credit to add. Must be a positive number."
    )
