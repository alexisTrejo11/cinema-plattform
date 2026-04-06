from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.wallet.application.results import WalletSummaryResult
from app.wallet.domain.value_objects import Money, PaymentDetails
from app.wallet.domain.entities.wallet import Wallet, WalletTransaction


class PaymentDetailsResponse(BaseModel):
    payment_method: str = Field(
        ...,
        description="The payment method used (e.g., 'card', 'transfer', 'crypto').",
        json_schema_extra={"example": "card"},
    )
    payment_id: UUID = Field(
        ...,
        description="The unique identifier for the external payment.",
        json_schema_extra={"example": "d1e2f3a4-b5c6-7890-1234-567890abcdef"},
    )

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_domain(cls, payment_details: "PaymentDetails") -> "PaymentDetailsResponse":
        return cls(
            payment_method=payment_details.payment_method,
            payment_id=payment_details.payment_id,
        )


class WalletTransactionResponse(BaseModel):
    transaction_id: UUID = Field(
        ...,
        description="The unique identifier for the wallet transaction.",
        json_schema_extra={"example": "a0b1c2d3-e4f5-6789-0123-456789abcdef"},
    )
    wallet_id: UUID = Field(
        ...,
        description="The identifier of the associated wallet.",
        json_schema_extra={"example": "b1c2d3e4-f5a6-7890-1234-567890abcdef"},
    )
    amount: str = Field(
        ...,
        description="The amount and currency of the transaction.",
        json_schema_extra={"example": {"amount": 50.00, "currency": "MXN"}},
    )
    transaction_type: str = Field(
        ...,
        description="The type of transaction (e.g., 'CREDIT', 'DEBIT').",
        json_schema_extra={"example": "CREDIT"},
    )
    payment_details: Optional[PaymentDetailsResponse] = Field(
        None,
        description="Optional details about the payment, if applicable.",
        json_schema_extra={
            "example": {
                "payment_method": "transfer",
                "payment_id": "c1d2e3f4-a5b6-7890-1234-567890abcdef",
            }
        },
    )
    timestamp: datetime = Field(
        ...,
        description="The timestamp when the transaction occurred (ISO 8601 format).",
        json_schema_extra={"example": "2024-07-15T19:00:00.123456Z"},
    )

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def generate(cls, transaction: "WalletTransaction") -> "WalletTransactionResponse":
        payment_details_dto = (
            PaymentDetailsResponse.from_domain(transaction.payment_details)
            if transaction.payment_details
            else None
        )

        return cls(
            transaction_id=transaction.transaction_id.value,
            wallet_id=transaction.wallet_id.value,
            amount=transaction.amount.display(),
            transaction_type=transaction.transaction_type.value,
            payment_details=payment_details_dto,
            timestamp=transaction.timestamp,
        )

    @classmethod
    def from_domain(cls, transaction: "WalletTransaction") -> "WalletTransactionResponse":
        return cls.generate(transaction)


class TransactionTypeSummaryRow(BaseModel):
    transaction_type: str
    count: int
    total_amount: str


class WalletSummaryResponse(BaseModel):
    wallet_id: UUID
    user_id: UUID
    balance: str
    currency: str
    total_transactions: int
    by_transaction_type: List[TransactionTypeSummaryRow]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_result(cls, result: WalletSummaryResult) -> "WalletSummaryResponse":
        return cls(
            wallet_id=result.wallet_id,
            user_id=result.user_id,
            balance=result.balance_display,
            currency=result.currency,
            total_transactions=result.total_transactions,
            by_transaction_type=[
                TransactionTypeSummaryRow(
                    transaction_type=row.transaction_type.value,
                    count=row.count,
                    total_amount=f"{row.total_amount} {result.currency}",
                )
                for row in result.by_transaction_type
            ],
        )


class WalletResponse(BaseModel):
    id: UUID = Field(
        ...,
        description="The unique identifier of the wallet.",
        json_schema_extra={"example": "b1c2d3e4-f5a6-7890-1234-567890abcdef"},
    )
    user_id: UUID = Field(
        ...,
        description="The ID of the user to whom this wallet belongs.",
        json_schema_extra={"example": "1a2b3c4d-5e6f-7890-1234-567890abcdef"},
    )
    balance: str = Field(
        ...,
        description="The current balance of the wallet, including amount and currency.",
        json_schema_extra={"example": "1250.75 USD"},
    )

    transactions: List[WalletTransactionResponse] = Field(
        ...,
        description="A list of recent transactions associated with this wallet. Can be empty.",
        json_schema_extra={
            "example": [
                {
                    "transaction_id": "a0b1c2d3-e4f5-6789-0123-456789abcdef",
                    "wallet_id": "b1c2d3e4-f5a6-7890-1234-567890abcdef",
                    "amount": {"amount": 50.00, "currency": "MXN"},
                    "transaction_type": "CREDIT",
                    "payment_details": {
                        "payment_method": "card",
                        "payment_id": "d1e2f3a4-b5c6-7890-1234-567890abcdef",
                    },
                    "timestamp": "2024-07-15T19:00:00.123456Z",
                }
            ]
        },
    )

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_domain(cls, wallet: Wallet):
        transactions = []
        if wallet.transactions and len(wallet.transactions) > 0:
            transactions = [
                WalletTransactionResponse.from_domain(transaction)
                for transaction in wallet.transactions
            ]

        return cls(
            id=wallet.id.value,
            user_id=wallet.user_id.value,
            transactions=transactions,
            balance=wallet.display_balance(),
        )


class BuyCreditDetails(BaseModel):
    """
    Response DTO for buying credit and adding it to a wallet.
    Provides an overview of the updated wallet balance and the specific credit transaction.
    """

    id: UUID = Field(
        ...,
        description="The unique identifier of the wallet.",
        json_schema_extra={"example": "b1c2d3e4-f5a6-7890-1234-567890abcdef"},
    )
    user_id: UUID = Field(
        ...,
        description="The ID of the user who owns this wallet.",
        json_schema_extra={"example": "1a2b3c4d-5e6f-7890-1234-567890abcdef"},
    )
    balance: Decimal = (
        Field(  # Note: This is Decimal, while WalletResponse.balance is str. Be consistent.
            ...,
            description="The new balance of the wallet after the credit purchase.",
            json_schema_extra={"example": 1500.00},
        )
    )
    transaction: WalletTransactionResponse = Field(
        ...,
        description="Details of the credit transaction that added funds to the wallet.",
        json_schema_extra={
            "example": {
                "transaction_id": "a0b1c2d3-e4f5-6789-0123-456789abcdef",
                "wallet_id": "b1c2d3e4-f5a6-7890-1234-567890abcdef",
                "amount": {"amount": 250.00, "currency": "USD"},
                "transaction_type": "CREDIT",
                "payment_details": {
                    "payment_method": "card",
                    "payment_id": "e1f2g3h4-i5j6-7890-1234-567890abcdef",
                },
                "timestamp": "2024-07-15T19:15:30.456789Z",
            }
        },
    )

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_domain(cls, wallet: Wallet, transaction: WalletTransaction):
        return cls(
            id=wallet.id.value,
            user_id=wallet.user_id.value,
            balance=wallet.balance.amount + " " + transaction.amount.currency,
            transaction=WalletTransactionResponse.from_domain(transaction),
        )


class WalletBuyDetails(BaseModel):
    """
    Response DTO for a purchase operation from a wallet.
    Provides an overview of the updated wallet balance and the specific debit transaction.
    """

    id: UUID = Field(
        ...,
        description="The unique identifier of the wallet.",
        json_schema_extra={"example": "b1c2d3e4-f5a6-7890-1234-567890abcdef"},
    )
    user_id: UUID = Field(
        ...,
        description="The ID of the user who owns this wallet.",
        json_schema_extra={"example": "1a2b3c4d-5e6f-7890-1234-567890abcdef"},
    )
    balance: Decimal = (
        Field(  # Note: This is Decimal, while WalletResponse.balance is str. Be consistent.
            ...,
            description="The new balance of the wallet after the purchase.",
            json_schema_extra={"example": 900.00},
        )
    )
    transaction: WalletTransactionResponse = Field(
        ...,
        description="Details of the debit transaction that subtracted funds from the wallet for the purchase.",
        json_schema_extra={
            "example": {
                "transaction_id": "f0g1h2i3-j4k5-6789-0123-456789abcdef",
                "wallet_id": "b1c2d3e4-f5a6-7890-1234-567890abcdef",
                "amount": {"amount": 350.75, "currency": "USD"},
                "transaction_type": "DEBIT",
                "payment_details": {
                    "payment_method": "internal_purchase",  # Example for an internal purchase
                    "payment_id": "f1g2h3i4-j5k6-7890-1234-567890abcdef",
                },
                "timestamp": "2024-07-15T19:20:15.987654Z",
            }
        },
    )

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def generate(cls, wallet: Wallet, transaction: WalletTransaction):
        return cls(
            id=wallet.id.value,
            user_id=wallet.user_id.value,
            balance=wallet.balance.amount + " " + wallet.balance.currency.value,
            transaction=WalletTransactionResponse.from_domain(transaction),
        )


class PayResponse(BaseModel):
    """
    DTO for initiating a payment request from a wallet.
    This model defines the input parameters for a payment operation.
    """

    wallet_id: UUID = Field(
        ...,
        description="The ID of the wallet from which the payment will be made.",
        json_schema_extra={"example": "b1c2d3e4-f5a6-7890-1234-567890abcdef"},
    )
    amount: float = (
        Field(  # Note: It's often better to use Decimal for financial amounts to avoid float precision issues.
            ...,
            gt=0,
            description="The amount to be paid. Must be a positive number.",
            json_schema_extra={"example": 75.25},
        )
    )
    # Consider adding currency if the wallet can handle multiple currencies,
    # or if the payment needs to specify it.
    # currency: str = Field(..., description="The currency of the payment (e.g., USD, MXN)", example="USD")

    model_config = ConfigDict(
        from_attributes=True
    )  # Ensure this is also Pydantic v2 config
