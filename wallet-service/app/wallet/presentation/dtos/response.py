from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.wallet.domain.value_objects import Money, PaymentDetails
from app.wallet.domain.entities.wallet import Wallet, WalletTransaction

class MoneyResponse(BaseModel):
    amount: Decimal = Field(..., description="Monto de la transacción")
    currency: str = Field(..., description="Moneda de la transacción (ej. USD, MXN)")

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_domain(cls, money: "Money") -> "MoneyResponse":
        return cls(amount=money.amount, currency=money.currency.value)


class PaymentDetailsResponse(BaseModel):
    payment_method: str = Field(
        ..., description="Método de pago (ej. 'card', 'transfer')"
    )
    payment_id: UUID = Field(..., description="Identificador único del pago externo")

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_domain(cls, payment_details: "PaymentDetails") -> "PaymentDetailsResponse":
        return cls(
            payment_method=payment_details.payment_method,
            payment_id=payment_details.payment_id,
        )


class WalletTransactionResponse(BaseModel):
    transaction_id: UUID = Field(
        ..., description="Identificador único de la transacción"
    )
    wallet_id: UUID = Field(..., description="Identificador de la billetera asociada")
    amount: MoneyResponse = Field(..., description="Monto y moneda de la transacción")
    transaction_type: str = Field(
        ..., description="Tipo de transacción (ej. CREDIT, DEBIT)"
    )
    payment_details: Optional[PaymentDetailsResponse] = Field(
        None, description="Detalles opcionales del pago"
    )
    timestamp: datetime = Field(..., description="Marca de tiempo de la transacción")

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_domain(
        cls, transaction: "WalletTransaction"
    ) -> "WalletTransactionResponse":

        money_dto = MoneyResponse.from_domain(transaction.amount)

        payment_details_dto = (
            PaymentDetailsResponse.from_domain(transaction.payment_details)
            if transaction.payment_details
            else None
        )

        return cls(
            transaction_id=transaction.transaction_id,
            wallet_id=transaction.wallet_id.value,
            amount=money_dto,
            transaction_type=transaction.transaction_type.value,
            payment_details=payment_details_dto,
            timestamp=transaction.timestamp,
        )



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


class PayResponse(BaseModel):
    """DTO for making a payment from a wallet."""

    wallet_id: UUID = Field(..., description="The ID of the wallet to pay from.")
    amount: float = Field(
        ..., gt=0, description="The amount to pay. Must be a positive number."
    )
