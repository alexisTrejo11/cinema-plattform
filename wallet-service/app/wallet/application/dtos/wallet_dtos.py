from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from app.user.domain.value_objects import UserId
from app.user.application.dtos import PydanticUserId
from app.wallet.domain.value_objects import Money, PaymentDetails, Currency
from app.wallet.domain.enums import TransactionType
from app.wallet.domain.entities.wallet import Wallet, WalletTransaction
from decimal import Decimal
from .transaction_dtos import WalletTransactionResponse, MoneyResponse


class WalletResponse(BaseModel):
    """DTO for wallet information."""

    id: UUID
    user_id: UUID
    balance: MoneyResponse
    transactions: Optional[List[WalletTransactionResponse]] = []

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_domain(cls, wallet: Wallet):
        transactions = []
        if len(wallet.transactions) > 1:
            transactions = [
                WalletTransactionResponse.from_domain(transaction)
                for transaction in wallet.transactions
            ]

        return cls(
            id=wallet.id.value,
            user_id=wallet.user_id.value,
            transactions=transactions,
            balance=MoneyResponse(
                amount=wallet.balance.amount, currency=wallet.balance.currency.value
            ),
        )


# Create Response for transaction
class BuyCreditResponse(BaseModel):
    """DTO for wallet information."""

    id: UUID
    user_id: UUID
    balance: Decimal
    transaction: WalletTransactionResponse

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_domain(cls, wallet: Wallet, transaction: WalletTransaction):
        return cls(
            id=wallet.id.value,
            user_id=wallet.user_id.value,
            balance=wallet.balance.amount,
            transaction=WalletTransactionResponse.from_domain(transaction),
        )


class WalletBuyResponse(BaseModel):
    """DTO for wallet information."""

    id: UUID
    user_id: UUID
    balance: Decimal
    transaction: WalletTransactionResponse

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_domain(cls, wallet: Wallet, transaction: WalletTransaction):
        return cls(
            id=wallet.id.value,
            user_id=wallet.user_id.value,
            balance=wallet.balance.amount,
            transaction=WalletTransactionResponse.from_domain(transaction),
        )


class CreateWalletResponse(BaseModel):
    """DTO for creating a new wallet."""

    user_id: PydanticUserId = Field(
        ..., description="The ID of the user who will own the new wallet."
    )


class CreateWalletCommand(BaseModel):
    """DTO for creating a new wallet."""

    user_id: UserId
    
    
class AddCreditRequest(BaseModel):
    """DTO for adding credit to a wallet."""

    wallet_id: UUID = Field(..., description="The ID of the wallet to add credit to.")
    amount: float = Field(
        ..., gt=0, description="The amount of credit to add. Must be a positive number."
    )
    currency: Currency = Field(..., description="MXN OR USD")
    model_config = ConfigDict(from_attributes=True)


class AddCreditCommand(BaseModel):
    """DTO for adding credit to a wallet."""

    wallet_id: UUID = Field(..., description="The ID of the wallet to add credit to.")
    payment_details: PaymentDetails
    amount: Money


class PayResponse(BaseModel):
    """DTO for making a payment from a wallet."""

    wallet_id: UUID = Field(..., description="The ID of the wallet to pay from.")
    amount: float = Field(
        ..., gt=0, description="The amount to pay. Must be a positive number."
    )


class PayWithWalletCommand(BaseModel):
    """DTO for making a payment from a wallet."""

    wallet_id: UUID
    payment_details: PaymentDetails
    amount: Money
