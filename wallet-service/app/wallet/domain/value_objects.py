import uuid
from decimal import Decimal
from typing import Union
from app.wallet.domain.exceptions import (
    InvalidTransactionAmountError,
    UnsupportedCurrencyError,
)
from app.wallet.domain.enums import Currency


class WalletId:
    def __init__(self, value: uuid.UUID) -> None:
        if not isinstance(value, uuid.UUID):
            raise ValueError("WalletId must be a valid UUID.")
        self.value = value

    @classmethod
    def from_string(cls, value: str) -> "WalletId":
        try:
            return cls(uuid.UUID(value))
        except ValueError as e:
            raise ValueError(f"Invalid UUID string for WalletId: {value}") from e

    def to_string(self) -> str:
        return str(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WalletId):
            return NotImplemented
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return f"WalletId({self.value})"


class Money:
    def __init__(self, amount: Union[Decimal, str, float], currency: Currency):
        if not isinstance(amount, Decimal):
            try:
                self.amount = Decimal(str(amount))
            except Exception as e:
                raise InvalidTransactionAmountError(
                    "Amount must be a valid number."
                ) from e
        else:
            self.amount = amount

        if self.amount < Decimal("0"):
            raise InvalidTransactionAmountError("Amount must be positive.")

        if not isinstance(currency, Currency):
            raise TypeError("Currency must be an instance of Currency Enum.")
        self.currency = currency

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise UnsupportedCurrencyError(
                "Cannot add Money with different currencies."
            )
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise UnsupportedCurrencyError(
                "Cannot subtract Money with different currencies."
            )
        return Money(self.amount - other.amount, self.currency)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other: "Money") -> bool:
        if self.currency != other.currency:
            raise UnsupportedCurrencyError(
                "Cannot compare Money with different currencies."
            )
        return self.amount < other.amount

    def __le__(self, other: "Money") -> bool:
        if self.currency != other.currency:
            raise UnsupportedCurrencyError(
                "Cannot compare Money with different currencies."
            )
        return self.amount <= other.amount

    def __gt__(self, other: "Money") -> bool:
        if self.currency != other.currency:
            raise UnsupportedCurrencyError(
                "Cannot compare Money with different currencies."
            )
        return self.amount > other.amount

    def __ge__(self, other: "Money") -> bool:
        if self.currency != other.currency:
            raise UnsupportedCurrencyError(
                "Cannot compare Money with different currencies."
            )
        return self.amount >= other.amount

    def __repr__(self) -> str:
        return f"Money({self.amount} {self.currency.value})"


class PaymentDetails:
    def __init__(self, payment_method: str, payment_id: uuid.UUID):
        self.payment_method = payment_method
        self.payment_id = payment_id

    def __repr__(self):
        return (
            f"PaymentDeal(payment_id={self.payment_id}, method={self.payment_method})"
        )
