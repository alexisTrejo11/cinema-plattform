"""
Domain Value Objects

Immutable objects that represent domain concepts without identity.
Value objects encapsulate business rules and provide type safety.
"""

from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from .excpetions import InvalidPaymentAmountException


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


@dataclass(frozen=True)
class Money:
    """
    Money value object representing monetary amounts with currency.
    
    Ensures proper handling of monetary calculations and currency consistency.
    """
    amount: Decimal
    currency: Currency
    
    def __post_init__(self):
        """Validate money constraints."""
        if self.amount < 0:
            raise InvalidPaymentAmountException(float(self.amount), 0.0)
        
        # Ensure proper decimal precision (2 decimal places for most currencies)
        object.__setattr__(self, 'amount', self.amount.quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        ))
    
    @classmethod
    def zero(cls, currency: Currency = Currency.USD) -> Money:
        """Create a zero money value."""
        return cls(Decimal('0.00'), currency)
    
    @classmethod
    def from_float(cls, amount: float, currency: Currency = Currency.USD) -> Money:
        """Create Money from float value."""
        return cls(Decimal(str(amount)), currency)
    
    def add(self, other: Money) -> Money:
        """Add two money amounts (must be same currency)."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(self.amount + other.amount, self.currency)
    
    def subtract(self, other: Money) -> Money:
        """Subtract two money amounts (must be same currency)."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot subtract {other.currency} from {self.currency}")
        result_amount = self.amount - other.amount
        return Money(result_amount, self.currency)
    
    def multiply(self, factor: Decimal) -> Money:
        """Multiply money by a factor."""
        return Money(self.amount * factor, self.currency)
    
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


@dataclass(frozen=True)
class PaymentId:
    """Payment identifier value object."""
    value: UUID
    
    @classmethod
    def generate(cls) -> PaymentId:
        """Generate a new payment ID."""
        return cls(uuid4())
    
    @classmethod
    def from_string(cls, id_str: str) -> PaymentId:
        """Create PaymentId from string."""
        return cls(UUID(id_str))
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class WalletId:
    """Wallet identifier value object."""
    value: UUID
    
    @classmethod
    def generate(cls) -> WalletId:
        """Generate a new wallet ID."""
        return cls(uuid4())
    
    @classmethod
    def from_string(cls, id_str: str) -> WalletId:
        """Create WalletId from string."""
        return cls(UUID(id_str))
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class TransactionId:
    """Transaction identifier value object."""
    value: UUID
    
    @classmethod
    def generate(cls) -> TransactionId:
        """Generate a new transaction ID."""
        return cls(uuid4())
    
    @classmethod
    def from_string(cls, id_str: str) -> TransactionId:
        """Create TransactionId from string."""
        return cls(UUID(id_str))
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class UserId:
    """User identifier value object."""
    value: UUID
    
    @classmethod
    def from_string(cls, id_str: str) -> UserId:
        """Create UserId from string."""
        return cls(UUID(id_str))
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class PaymentReference:
    """
    External payment reference from payment gateway.
    
    Stores the reference ID from external payment providers
    like Stripe, PayPal, etc.
    """
    provider: str
    reference_id: str
    
    def __str__(self) -> str:
        return f"{self.provider}:{self.reference_id}"


@dataclass(frozen=True)
class PaymentMetadata:
    """
    Additional payment metadata.
    
    Stores contextual information about the payment
    like ticket IDs, showtime information, etc.
    """
    ticket_ids: Optional[list[str]] = None
    showtime_id: Optional[str] = None
    seat_numbers: Optional[list[str]] = None
    food_items: Optional[list[dict]] = None
    pickup_location: Optional[str] = None
    special_instructions: Optional[str] = None
    
    def has_tickets(self) -> bool:
        """Check if payment includes tickets."""
        return self.ticket_ids is not None and len(self.ticket_ids) > 0
    
    def has_food_items(self) -> bool:
        """Check if payment includes food items."""
        return self.food_items is not None and len(self.food_items) > 0
