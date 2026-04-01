"""
Domain Value Objects

Immutable objects that represent domain concepts without identity.
Value objects encapsulate business rules and provide type safety.
"""

from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
import uuid

from pydantic import BaseModel, ConfigDict, model_validator

from .exceptions import InvalidPaymentAmountException


class ID(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: uuid.UUID

    def __str__(self):
        return str(self.value)

    @staticmethod
    def generate():
        return ID(value=uuid.uuid4())


class Currency(str, Enum):
    """Supported currencies for payments."""

    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"


class PaymentMethod(str, Enum):
    """Available payment methods."""

    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    WALLET = "wallet"
    BANK_TRANSFER = "bank_transfer"


class PaymentStatus(str, Enum):
    """Payment processing status."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"


class PaymentType(str, Enum):
    """Types of payments supported."""

    TICKET_PURCHASE = "ticket_purchase"
    FOOD_PURCHASE = "food_purchase"
    MERCHANDISE_PURCHASE = "merchandise_purchase"
    WALLET_TOPUP = "wallet_topup"
    SUBSCRIPTION = "subscription"
    REFUND = "refund"


class TransactionType(str, Enum):
    """Transaction types for wallet operations."""

    CREDIT = "credit"
    DEBIT = "debit"
    REFUND = "refund"
    TRANSFER = "transfer"
    FEE = "fee"


class WalletStatus(str, Enum):
    """Wallet status enumeration."""

    ACTIVE = "active"
    SUSPENDED = "suspended"
    FROZEN = "frozen"
    CLOSED = "closed"


class Money(BaseModel):
    """
    Money value object representing monetary amounts with currency.

    Ensures proper handling of monetary calculations and currency consistency.
    """

    model_config = ConfigDict(frozen=True)

    amount: Decimal
    currency: Currency

    @model_validator(mode="after")
    def validate_money(self) -> Money:
        """Validate money constraints."""
        if self.amount < 0:
            raise InvalidPaymentAmountException(float(self.amount), 0.0)

        object.__setattr__(
            self,
            "amount",
            self.amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        )
        return self

    @classmethod
    def zero(cls, currency: Currency = Currency.USD) -> Money:
        """Create a zero money value."""
        return cls(amount=Decimal("0.00"), currency=currency)

    @classmethod
    def from_float(cls, amount: float, currency: Currency = Currency.USD) -> Money:
        """Create Money from float value."""
        return cls(amount=Decimal(str(amount)), currency=currency)

    def add(self, other: Money) -> Money:
        """Add two money amounts (must be same currency)."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def subtract(self, other: Money) -> Money:
        """Subtract two money amounts (must be same currency)."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot subtract {other.currency} from {self.currency}")
        result_amount = self.amount - other.amount
        return Money(amount=result_amount, currency=self.currency)

    def multiply(self, factor: Decimal) -> Money:
        """Multiply money by a factor."""
        return Money(amount=self.amount * factor, currency=self.currency)

    def is_positive(self) -> bool:
        """Check if amount is positive."""
        return self.amount > 0

    def is_zero(self) -> bool:
        """Check if amount is zero."""
        return self.amount == 0

    def is_greater_than(self, other: Money) -> bool:
        """Check if this amount is greater than another."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot compare {self.currency} and {other.currency}")
        return self.amount > other.amount

    def is_greater_than_or_equal(self, other: Money) -> bool:
        """Check if this amount is greater than or equal to another."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot compare {self.currency} and {other.currency}")
        return self.amount >= other.amount

    def to_float(self) -> float:
        """Convert to float (use with caution)."""
        return float(self.amount)

    def __str__(self) -> str:
        return f"{self.amount} {self.currency.value}"


class PaymentId(BaseModel):
    """Payment identifier value object."""

    model_config = ConfigDict(frozen=True)

    value: UUID

    @classmethod
    def generate(cls) -> PaymentId:
        """Generate a new payment ID."""
        return cls(value=uuid4())

    @classmethod
    def from_string(cls, id_str: str) -> PaymentId:
        """Create PaymentId from string."""
        return cls(value=UUID(id_str))

    def __str__(self) -> str:
        return str(self.value)


class WalletId(BaseModel):
    """Wallet identifier value object."""

    model_config = ConfigDict(frozen=True)

    value: UUID

    @classmethod
    def generate(cls) -> WalletId:
        """Generate a new wallet ID."""
        return cls(value=uuid4())

    @classmethod
    def from_string(cls, id_str: str) -> WalletId:
        """Create WalletId from string."""
        return cls(value=UUID(id_str))

    def __str__(self) -> str:
        return str(self.value)


class TransactionId(BaseModel):
    """Transaction identifier value object."""

    model_config = ConfigDict(frozen=True)

    value: UUID

    @classmethod
    def generate(cls) -> TransactionId:
        """Generate a new transaction ID."""
        return cls(value=uuid4())

    @classmethod
    def from_string(cls, id_str: str) -> TransactionId:
        """Create TransactionId from string."""
        return cls(value=UUID(id_str))

    def __str__(self) -> str:
        return str(self.value)


class UserId(BaseModel):
    """User identifier value object."""

    model_config = ConfigDict(frozen=True)

    value: UUID

    @classmethod
    def from_string(cls, id_str: str) -> UserId:
        """Create UserId from string."""
        return cls(value=UUID(id_str))

    def __str__(self) -> str:
        return str(self.value)


class PaymentReference(BaseModel):
    """
    External payment reference from payment gateway.

    Stores the reference ID from external payment providers
    like Stripe, PayPal, etc.
    """

    model_config = ConfigDict(frozen=True)

    provider: str
    reference_id: str

    def __str__(self) -> str:
        return f"{self.provider}:{self.reference_id}"


class PaymentMetadata(BaseModel):
    """
    Additional payment metadata.

    Stores contextual information about the payment
    like ticket IDs, showtime information, etc.
    """

    model_config = ConfigDict(frozen=True)

    ticket_ids: Optional[list[str]] = None
    show_id: Optional[str] = None
    showtime_id: Optional[str] = None
    # UTC: when the screening starts; used for refund rules (e.g. no refund after show).
    show_starts_at: Optional[datetime] = None
    seat_numbers: Optional[list[str]] = None
    food_items: Optional[list[dict]] = None
    items: Optional[list[dict]] = None
    order_id: Optional[str] = None
    plan_id: Optional[str] = None
    wallet_id: Optional[str] = None
    pickup_location: Optional[str] = None
    special_instructions: Optional[str] = None

    def has_tickets(self) -> bool:
        """Check if payment includes tickets."""
        return self.ticket_ids is not None and len(self.ticket_ids) > 0

    def has_food_items(self) -> bool:
        """Check if payment includes food items."""
        return self.food_items is not None and len(self.food_items) > 0


class Card(BaseModel):
    """Card details; ``stripe_payment_method_id`` is the Stripe ``pm_xxx`` after tokenization."""

    model_config = ConfigDict(frozen=True)

    card_holder: str
    card_number: str
    cvv: str
    expiration_month: str
    expiration_year: str
    stripe_payment_method_id: Optional[str] = None


class PaymentProvider(str, Enum):
    """Supported external payment providers."""

    STRIPE = "stripe"
    PAYPAL = "paypal"
    ADEYEN = "adyen"
    INTERNAL = "internal"  # For internal wallet payments


class PaymentMethodType(str, Enum):
    """Logical category of the payment method."""

    CARD = "card"  # Crédito/Débito
    CASH = "cash"  # Oxxo, 7-Eleven, etc.
    BANK_TRANSFER = "bank"  # SPEI, SEPA, SWIFT
    DIGITAL_WALLET = "wallet"  # Apple Pay, Google Pay, Internal Wallet
