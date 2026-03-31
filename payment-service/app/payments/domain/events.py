"""
Domain Events

Represents things that happened in the domain that domain experts care about.
These events are used for event-driven architecture and inter-service communication.
"""

from __future__ import annotations

from typing import Dict, Any, Optional
from uuid import UUID, uuid4
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .value_objects import (
    PaymentId,
    WalletId,
    TransactionId,
    UserId,
    Money,
    PaymentType,
    TransactionType,
)


class DomainEvent(BaseModel):
    """Base class for all payment domain events."""

    model_config = ConfigDict(frozen=True)

    event_id: UUID = Field(default_factory=uuid4)
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    aggregate_id: Optional[UUID] = None
    version: int = 1

    def event_type(self) -> str:
        raise NotImplementedError

    def _get_event_data(self) -> Dict[str, Any]:
        raise NotImplementedError

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type(),
            "occurred_at": self.occurred_at.isoformat(),
            "aggregate_id": str(self.aggregate_id) if self.aggregate_id else None,
            "version": self.version,
            "data": self._get_event_data(),
        }


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
