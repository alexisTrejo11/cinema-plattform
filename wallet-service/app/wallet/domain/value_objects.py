import uuid
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator

from app.wallet.domain.enums import Currency
from app.wallet.domain.exceptions import (
    InvalidTransactionAmountError,
    UnsupportedCurrencyError,
)


class BaseUUIDValueObject(BaseModel):
    """Base class for immutable UUID-based identity value objects."""

    model_config = ConfigDict(frozen=True)

    value: uuid.UUID

    @classmethod
    def create(cls, value: uuid.UUID) -> "BaseUUIDValueObject":
        return cls(value=value)

    @classmethod
    def generate(cls) -> "BaseUUIDValueObject":
        return cls(value=uuid.uuid4())

    @classmethod
    def from_string(cls, value: str) -> "BaseUUIDValueObject":
        try:
            return cls(value=uuid.UUID(value))
        except ValueError as e:
            raise ValueError(f"Invalid UUID string for {cls.__name__}: {value}") from e

    def to_string(self) -> str:
        return str(self.value)


class WalletId(BaseUUIDValueObject):
    """Immutable unique identifier for a Wallet."""


class UserId(BaseUUIDValueObject):
    """Immutable unique identifier for a User."""


class WalletTransactionId(BaseUUIDValueObject):
    """Immutable unique identifier for a Wallet Transaction."""


class Money(BaseModel):
    """
    Immutable monetary value. Amount is always non-negative.
    Arithmetic operations return new Money instances (value-object semantics).
    Pydantic provides __eq__ and __hash__ via frozen=True.
    """

    model_config = ConfigDict(frozen=True)

    amount: Decimal
    currency: Currency

    @field_validator("amount", mode="before")
    @classmethod
    def coerce_and_validate_amount(cls, v) -> Decimal:
        # Coerce str/float/int to Decimal before the positive-amount check
        if not isinstance(v, Decimal):
            try:
                v = Decimal(str(v))
            except Exception as e:
                raise InvalidTransactionAmountError(
                    "Amount must be a valid number."
                ) from e
        if v < 0:
            raise InvalidTransactionAmountError("Amount cannot be negative.")
        return v

    # ── Arithmetic (return new instances — frozen model cannot mutate) ──────

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise UnsupportedCurrencyError(
                "Cannot add Money with different currencies."
            )
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise UnsupportedCurrencyError(
                "Cannot subtract Money with different currencies."
            )
        return Money(amount=self.amount - other.amount, currency=self.currency)

    # ── Ordering (Pydantic frozen only provides __eq__/__hash__, not ordering) ─

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


class PaymentDetails(BaseModel):
    """Immutable external payment reference. Pydantic provides __repr__ and __eq__."""

    model_config = ConfigDict(frozen=True)

    payment_method: str
    payment_id: uuid.UUID


class Charge(BaseModel):
    """
    Represents the magnitude of a deduction (always a positive value).
    Kept separate from Money to make debit intent explicit at the type level.
    Pydantic coerces str/float/int to Decimal; no sign restriction because
    negative values may appear when building transaction records internally.
    """

    model_config = ConfigDict(frozen=True)

    amount: Decimal
    currency: Currency

    @field_validator("amount", mode="before")
    @classmethod
    def coerce_amount(cls, v) -> Decimal:
        if not isinstance(v, Decimal):
            try:
                return Decimal(str(v))
            except Exception as e:
                raise InvalidTransactionAmountError(
                    "Amount must be a valid number."
                ) from e
        return v
