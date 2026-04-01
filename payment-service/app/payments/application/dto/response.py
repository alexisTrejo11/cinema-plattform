from typing import Any, Dict, List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class PayTicketResponse:
    """Response model for ticket payment."""

    def __init__(
        self,
        success: bool,
        payment_id: Optional[UUID] = None,
        ticket_ids: Optional[list[str]] = None,
        amount_paid: Optional[float] = None,
        transaction_reference: Optional[str] = None,
        confirmation_code: Optional[str] = None,
        message: str = "",
        error_code: Optional[str] = None,
    ):
        self.success = success
        self.payment_id = payment_id
        self.ticket_ids = ticket_ids
        self.amount_paid = amount_paid
        self.transaction_reference = transaction_reference
        self.confirmation_code = confirmation_code
        self.message = message
        self.error_code = error_code


class PaymentHistoryItem(BaseModel):
    """Individual payment history item."""

    payment_id: UUID
    user_id: UUID
    amount: float
    currency: str
    payment_method: str
    payment_type: str
    status: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    failure_reason: Optional[str] = None
    refunded_amount: float = 0.0
    refund_reasons: List[str] = []
    refunded_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class PaymentHistoryItemBuilder:
    def __init__(self) -> None:
        """Initialize with default values for all fields."""
        self._payment_id = UUID(int=0)
        self._user_id = UUID(int=0)
        self._amount = 0.0
        self._currency = "USD"
        self._payment_method = "credit_card"
        self._payment_type = "purchase"
        self._status = "pending"
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
        self._completed_at = None
        self._failure_reason = None
        self._refunded_amount = 0.0
        self._refund_reasons: List[str] = []
        self._refunded_at = None
        self._metadata = None

    def set_payment_id(self, payment_id: UUID) -> "PaymentHistoryItemBuilder":
        """Set the unique payment identifier."""
        self._payment_id = payment_id
        return self

    def set_user_id(self, user_id: UUID) -> "PaymentHistoryItemBuilder":
        """Set the user identifier associated with the payment."""
        self._user_id = user_id
        return self

    def set_amount(self, amount: float) -> "PaymentHistoryItemBuilder":
        """Set the payment amount (must be positive)."""
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        self._amount = amount
        return self

    def set_currency(self, currency: str) -> "PaymentHistoryItemBuilder":
        """Set the currency code (ISO format)."""
        if len(currency) != 3:
            raise ValueError("Currency must be 3-character ISO code")
        self._currency = currency.upper()
        return self

    def set_payment_method(self, payment_method: str) -> "PaymentHistoryItemBuilder":
        """Set the payment method used."""
        self._payment_method = payment_method
        return self

    def set_payment_type(self, payment_type: str) -> "PaymentHistoryItemBuilder":
        """Set the type of payment (purchase/refund/subscription)."""
        self._payment_type = payment_type
        return self

    def set_status(self, status: str) -> "PaymentHistoryItemBuilder":
        """Set the payment status."""
        self._status = status
        return self

    def set_timestamps(
        self,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
    ) -> "PaymentHistoryItemBuilder":
        """Set multiple timestamp fields at once."""
        self._created_at = created_at or datetime.now()
        self._updated_at = updated_at or datetime.now()
        self._completed_at = completed_at
        return self

    def set_refund_details(
        self,
        refunded_amount: float = 0.0,
        refund_reasons: Optional[List[str]] = None,
        refunded_at: Optional[datetime] = None,
    ) -> "PaymentHistoryItemBuilder":
        """Configure refund-related fields."""
        self._refunded_amount = refunded_amount
        self._refund_reasons = list(refund_reasons or [])
        self._refunded_at = refunded_at
        return self

    def set_failure_details(
        self, failure_reason: Optional[str] = None
    ) -> "PaymentHistoryItemBuilder":
        """Set failure-related information."""
        self._failure_reason = failure_reason
        return self

    def set_metadata(
        self, metadata: Optional[Dict[str, Any]]
    ) -> "PaymentHistoryItemBuilder":
        """Set additional metadata dictionary."""
        self._metadata = metadata
        return self

    def build(self) -> PaymentHistoryItem:
        """Construct and validate the PaymentHistoryItem object."""
        return PaymentHistoryItem(
            payment_id=self._payment_id,
            user_id=self._user_id,
            amount=self._amount,
            currency=self._currency,
            payment_method=self._payment_method,
            payment_type=self._payment_type,
            status=self._status,
            created_at=self._created_at,
            updated_at=self._updated_at,
            completed_at=self._completed_at,
            failure_reason=self._failure_reason,
            refunded_amount=self._refunded_amount,
            refund_reasons=self._refund_reasons,
            refunded_at=self._refunded_at,
            metadata=self._metadata,
        )


class TransactionDetail(BaseModel):
    """Detailed transaction information."""

    transaction_id: UUID
    wallet_id: UUID
    user_id: UUID
    amount: float
    currency: str
    transaction_type: str
    description: str
    created_at: datetime
    processed_at: Optional[datetime] = None
    reference_id: Optional[str] = None
    related_transaction_id: Optional[UUID] = None
    balance_before: Optional[float] = None
    balance_after: Optional[float] = None
    is_reversed: bool = False
    reversal_reason: Optional[str] = None
    reversed_at: Optional[datetime] = None


class PaymentDetail(BaseModel):
    """Payment details for transaction context."""

    payment_id: UUID
    user_id: UUID
    amount: float
    currency: str
    payment_method: str
    payment_type: str
    status: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    failure_reason: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class WalletDetail(BaseModel):
    """Wallet details for transaction context."""

    wallet_id: UUID
    user_id: UUID
    current_balance: float
    currency: str
    status: str
    created_at: datetime
    updated_at: datetime
    last_transaction_at: Optional[datetime] = None


class AddCreditResult(BaseModel):
    wallet_id: UUID
    transaction_id: UUID
    user_id: UUID
    amount: float
    currency: str
    new_balance: float
    status: str
    message: str


class ProcessPaymentResult(BaseModel):
    """Result of payment processing."""

    payment_id: UUID
    status: str
    message: str
    transaction_reference: Optional[str] = None


class RefundPaymentResult(BaseModel):
    """Result of payment refund."""

    payment_id: UUID
    refund_amount: float
    status: str
    message: str
    transaction_reference: Optional[str] = None
    refunded_to_wallet: bool = False
