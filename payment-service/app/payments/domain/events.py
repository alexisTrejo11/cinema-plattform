"""
Domain Events

Represents things that happened in the domain that domain experts care about.
These events are used for event-driven architecture and inter-service communication.
"""

from typing import Dict, Any, Optional
from app.shared.events.base import DomainEvent

from .value_objects import (
    PaymentId,
    WalletId,
    TransactionId,
    UserId,
    Money,
    PaymentType,
    TransactionType,
)


class PaymentCreated(DomainEvent):
    """Event raised when a new payment is created."""

    payment_id: PaymentId
    user_id: UserId
    amount: Money
    payment_type: PaymentType
    metadata: Optional[Dict[str, Any]] = None

    def event_type(self) -> str:
        return "payment.created"

    def _get_event_data(self) -> Dict[str, Any]:
        return {
            "payment_id": str(self.payment_id),
            "user_id": str(self.user_id),
            "amount": self.amount.to_float(),
            "currency": self.amount.currency.value,
            "payment_type": self.payment_type.value,
            "metadata": self.metadata or {},
        }


class PaymentProcessingStarted(DomainEvent):
    """Event raised when payment processing begins."""

    payment_id: PaymentId
    user_id: UserId
    amount: Money
    payment_method: str

    def event_type(self) -> str:
        return "payment.processing_started"

    def _get_event_data(self) -> Dict[str, Any]:
        return {
            "payment_id": str(self.payment_id),
            "user_id": str(self.user_id),
            "amount": self.amount.to_float(),
            "currency": self.amount.currency.value,
            "payment_method": self.payment_method,
        }


class PaymentCompleted(DomainEvent):
    """Event raised when a payment is successfully completed."""

    payment_id: PaymentId
    user_id: UserId
    amount: Money
    payment_type: PaymentType
    transaction_reference: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def event_type(self) -> str:
        return "payment.completed"

    def _get_event_data(self) -> Dict[str, Any]:
        return {
            "payment_id": str(self.payment_id),
            "user_id": str(self.user_id),
            "amount": self.amount.to_float(),
            "currency": self.amount.currency.value,
            "payment_type": self.payment_type.value,
            "transaction_reference": self.transaction_reference,
            "metadata": self.metadata or {},
        }


class PaymentFailed(DomainEvent):
    """Event raised when a payment fails."""

    payment_id: PaymentId
    user_id: UserId
    amount: Money
    failure_reason: str
    error_code: Optional[str] = None

    def event_type(self) -> str:
        return "payment.failed"

    def _get_event_data(self) -> Dict[str, Any]:
        return {
            "payment_id": str(self.payment_id),
            "user_id": str(self.user_id),
            "amount": self.amount.to_float(),
            "currency": self.amount.currency.value,
            "failure_reason": self.failure_reason,
            "error_code": self.error_code,
        }


class PaymentCancelled(DomainEvent):
    """Event raised when a pending payment is cancelled (distinct from failure)."""

    payment_id: PaymentId
    user_id: UserId
    amount: Money
    reason: str

    def event_type(self) -> str:
        return "payment.cancelled"

    def _get_event_data(self) -> Dict[str, Any]:
        return {
            "payment_id": str(self.payment_id),
            "user_id": str(self.user_id),
            "amount": self.amount.to_float(),
            "currency": self.amount.currency.value,
            "reason": self.reason,
        }


class PaymentRefunded(DomainEvent):
    """Event raised when a payment is refunded."""

    payment_id: PaymentId
    user_id: UserId
    original_amount: Money
    refund_amount: Money
    refund_reason: str
    transaction_reference: Optional[str] = None

    def event_type(self) -> str:
        return "payment.refunded"

    def _get_event_data(self) -> Dict[str, Any]:
        return {
            "payment_id": str(self.payment_id),
            "user_id": str(self.user_id),
            "original_amount": self.original_amount.to_float(),
            "refund_amount": self.refund_amount.to_float(),
            "currency": self.original_amount.currency.value,
            "refund_reason": self.refund_reason,
            "transaction_reference": self.transaction_reference,
        }


class WalletCredited(DomainEvent):
    """Event raised when a wallet is credited."""

    wallet_id: WalletId
    user_id: UserId
    amount: Money
    previous_balance: Money
    new_balance: Money
    transaction_id: TransactionId
    description: str

    def event_type(self) -> str:
        return "wallet.credited"

    def _get_event_data(self) -> Dict[str, Any]:
        return {
            "wallet_id": str(self.wallet_id),
            "user_id": str(self.user_id),
            "amount": self.amount.to_float(),
            "previous_balance": self.previous_balance.to_float(),
            "new_balance": self.new_balance.to_float(),
            "currency": self.amount.currency.value,
            "transaction_id": str(self.transaction_id),
            "description": self.description,
        }


class WalletDebited(DomainEvent):
    """Event raised when a wallet is debited."""

    wallet_id: WalletId
    user_id: UserId
    amount: Money
    previous_balance: Money
    new_balance: Money
    transaction_id: TransactionId
    description: str

    def event_type(self) -> str:
        return "wallet.debited"

    def _get_event_data(self) -> Dict[str, Any]:
        return {
            "wallet_id": str(self.wallet_id),
            "user_id": str(self.user_id),
            "amount": self.amount.to_float(),
            "previous_balance": self.previous_balance.to_float(),
            "new_balance": self.new_balance.to_float(),
            "currency": self.amount.currency.value,
            "transaction_id": str(self.transaction_id),
            "description": self.description,
        }


class InsufficientFundsDetected(DomainEvent):
    """Event raised when wallet has insufficient funds."""

    wallet_id: WalletId
    user_id: UserId
    required_amount: Money
    available_balance: Money
    attempted_transaction_id: TransactionId

    def event_type(self) -> str:
        return "wallet.insufficient_funds"

    def _get_event_data(self) -> Dict[str, Any]:
        return {
            "wallet_id": str(self.wallet_id),
            "user_id": str(self.user_id),
            "required_amount": self.required_amount.to_float(),
            "available_balance": self.available_balance.to_float(),
            "currency": self.required_amount.currency.value,
            "attempted_transaction_id": str(self.attempted_transaction_id),
        }


class TransactionRecorded(DomainEvent):
    """Event raised when a new transaction is recorded."""

    transaction_id: TransactionId
    wallet_id: WalletId
    user_id: UserId
    amount: Money
    transaction_type: TransactionType
    description: str
    reference_id: Optional[str] = None

    def event_type(self) -> str:
        return "transaction.recorded"

    def _get_event_data(self) -> Dict[str, Any]:
        return {
            "transaction_id": str(self.transaction_id),
            "wallet_id": str(self.wallet_id),
            "user_id": str(self.user_id),
            "amount": self.amount.to_float(),
            "currency": self.amount.currency.value,
            "transaction_type": self.transaction_type.value,
            "description": self.description,
            "reference_id": self.reference_id,
        }


class TransactionReversed(DomainEvent):
    """Event raised when a transaction is reversed."""

    transaction_id: TransactionId
    wallet_id: WalletId
    user_id: UserId
    amount: Money
    transaction_type: TransactionType
    reversal_reason: str

    def event_type(self) -> str:
        return "transaction.reversed"

    def _get_event_data(self) -> Dict[str, Any]:
        return {
            "transaction_id": str(self.transaction_id),
            "wallet_id": str(self.wallet_id),
            "user_id": str(self.user_id),
            "amount": self.amount.to_float(),
            "currency": self.amount.currency.value,
            "transaction_type": self.transaction_type.value,
            "reversal_reason": self.reversal_reason,
        }


class PaymentMethodAdded(DomainEvent):
    """Event raised when a user registers a saved payment method."""

    payment_method_id: str
    user_id: UserId

    def event_type(self) -> str:
        return "payment_method.added"

    def _get_event_data(self) -> Dict[str, Any]:
        return {
            "payment_method_id": self.payment_method_id,
            "user_id": str(self.user_id),
        }


class PaymentMethodRemoved(DomainEvent):
    """Event raised when a saved payment method is removed (soft-deleted)."""

    payment_method_id: str
    user_id: UserId

    def event_type(self) -> str:
        return "payment_method.removed"

    def _get_event_data(self) -> Dict[str, Any]:
        return {
            "payment_method_id": self.payment_method_id,
            "user_id": str(self.user_id),
        }
