"""
Payment Domain Entity

Core business entity representing a payment in the cinema system.
Implements business rules and invariants for payment processing.
"""

from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import ClassVar, List, Optional

from pydantic import ConfigDict, Field, model_validator

from ..aggregate_root import AggregateRoot
from ..payment_settings import PAYMENT_EXPIRY_MINUTES
from ..value_objects import (
    PaymentId,
    UserId,
    Money,
    PaymentMethod,
    PaymentStatus,
    PaymentType,
    PaymentReference,
    PaymentMetadata,
)
from ..events import (
    DomainEvent,
    PaymentCreated,
    PaymentProcessingStarted,
    PaymentCompleted,
    PaymentFailed,
    PaymentCancelled,
    PaymentRefunded,
)
from ..exceptions import (
    PaymentAlreadyProcessedException,
    PaymentNotRefundableException,
    InvalidPaymentAmountException,
)


class Payment(AggregateRoot):
    """
    Payment aggregate root representing a payment transaction.

    Encapsulates all business rules related to payment processing,
    status management, and refund handling.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: PaymentId
    user_id: UserId

    amount: Money
    payment_method: PaymentMethod
    payment_type: PaymentType
    status: PaymentStatus

    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    external_reference: Optional[PaymentReference] = None
    metadata: Optional[PaymentMetadata] = None
    failure_reason: Optional[str] = None

    stripe_payment_intent_id: Optional[str] = (
        None  # Stripe pi_xxx for debugging and gateway calls
    )

    refunded_amount: Optional[Money] = None
    refund_reasons: List[str] = Field(default_factory=list)
    refunded_at: Optional[datetime] = None

    MIN_REFUND_AMOUNT: ClassVar[float] = 0.01
    MAX_PARTIAL_REFUND_DAYS: ClassVar[int] = 30

    @model_validator(mode="after")
    def init_and_validate(self) -> Payment:
        """Initialize derived fields and validate business rules."""
        if self.refunded_amount is None:
            self.refunded_amount = Money.zero(self.amount.currency)

        self._validate_payment_invariants()
        return self

    @classmethod
    def create(
        cls,
        user_id: UserId,
        amount: Money,
        payment_method: PaymentMethod,
        payment_type: PaymentType,
        metadata: Optional[PaymentMetadata] = None,
    ) -> Payment:
        """
        Factory method to create a new payment.

        Raises:
            InvalidPaymentAmountException: If amount is invalid
        """
        if amount.amount <= 0:
            raise InvalidPaymentAmountException(amount.to_float())

        payment_id = PaymentId.generate()
        now = datetime.now(timezone.utc)

        payment = cls(
            id=payment_id,
            user_id=user_id,
            amount=amount,
            payment_method=payment_method,
            payment_type=payment_type,
            status=PaymentStatus.PENDING,
            created_at=now,
            updated_at=now,
            expires_at=now + timedelta(minutes=PAYMENT_EXPIRY_MINUTES),
            metadata=metadata,
            refunded_amount=Money.zero(amount.currency),
            refund_reasons=[],
        )

        payment._add_event(
            PaymentCreated(
                payment_id=payment_id,
                user_id=user_id,
                amount=amount,
                payment_type=payment_type,
                metadata=metadata.model_dump() if metadata else None,
            )
        )

        return payment

    def start_processing(
        self, external_reference: Optional[PaymentReference] = None
    ) -> None:
        """
        Begin payment processing.

        Raises:
            PaymentAlreadyProcessedException: If payment is not in pending status
        """
        if not self.can_be_processed():
            raise PaymentAlreadyProcessedException(str(self.id), self.status.value)

        self.status = PaymentStatus.PROCESSING
        self.external_reference = external_reference
        self.updated_at = datetime.now(timezone.utc)

        self._add_event(
            PaymentProcessingStarted(
                payment_id=self.id,
                user_id=self.user_id,
                amount=self.amount,
                payment_method=self.payment_method.value,
            )
        )

    def complete(self, transaction_reference: Optional[str] = None) -> None:
        """
        Mark payment as completed successfully.

        Raises:
            PaymentAlreadyProcessedException: If payment cannot be completed
        """
        if not self.can_be_completed():
            raise PaymentAlreadyProcessedException(str(self.id), self.status.value)

        self.status = PaymentStatus.COMPLETED
        self.completed_at = datetime.now(timezone.utc)
        self.updated_at = self.completed_at

        if transaction_reference and self.external_reference:
            self.external_reference = PaymentReference(
                provider=self.external_reference.provider,
                reference_id=transaction_reference,
            )

        self._add_event(
            PaymentCompleted(
                payment_id=self.id,
                user_id=self.user_id,
                amount=self.amount,
                payment_type=self.payment_type,
                transaction_reference=transaction_reference,
                metadata=self.metadata.model_dump() if self.metadata else None,
            )
        )

    def fail(self, reason: str, error_code: Optional[str] = None) -> None:
        """
        Mark payment as failed.

        Raises:
            PaymentAlreadyProcessedException: If payment is already in a terminal state
        """
        if self.status in (
            PaymentStatus.COMPLETED,
            PaymentStatus.REFUNDED,
            PaymentStatus.CANCELLED,
        ):
            raise PaymentAlreadyProcessedException(str(self.id), self.status.value)

        self.status = PaymentStatus.FAILED
        self.failure_reason = reason
        self.updated_at = datetime.now(timezone.utc)

        self._add_event(
            PaymentFailed(
                payment_id=self.id,
                user_id=self.user_id,
                amount=self.amount,
                failure_reason=reason,
                error_code=error_code,
            )
        )

    def cancel(self, reason: str = "Cancelled by user") -> None:
        """
        Cancel a pending payment.

        Raises:
            PaymentAlreadyProcessedException: If payment cannot be cancelled
        """
        if not self.can_be_cancelled():
            raise PaymentAlreadyProcessedException(str(self.id), self.status.value)

        self.status = PaymentStatus.CANCELLED
        self.failure_reason = reason
        self.updated_at = datetime.now(timezone.utc)

        self._add_event(
            PaymentCancelled(
                payment_id=self.id,
                user_id=self.user_id,
                amount=self.amount,
                reason=reason,
            )
        )

    def refund(
        self,
        refund_amount: Money,
        reason: str,
        transaction_reference: Optional[str] = None,
    ) -> None:
        """
        Process a refund for this payment.

        Raises:
            PaymentNotRefundableException: If payment cannot be refunded
        """
        if not self.can_be_refunded():
            raise PaymentNotRefundableException(
                str(self.id), "Payment is not in refundable state"
            )

        if not self._is_valid_refund_amount(refund_amount):
            raise PaymentNotRefundableException(
                str(self.id),
                f"Invalid refund amount: {refund_amount}",
            )

        if not self._is_within_refund_window():
            raise PaymentNotRefundableException(
                str(self.id),
                "Refund window has expired",
            )

        new_refunded_amount = self.refunded_amount.add(refund_amount)
        self.refunded_amount = new_refunded_amount
        self.refund_reasons = [*self.refund_reasons, reason]
        self.refunded_at = datetime.now(timezone.utc)
        self.updated_at = self.refunded_at

        if new_refunded_amount.is_greater_than_or_equal(self.amount):
            self.status = PaymentStatus.REFUNDED
        else:
            self.status = PaymentStatus.PARTIALLY_REFUNDED

        self._add_event(
            PaymentRefunded(
                payment_id=self.id,
                user_id=self.user_id,
                original_amount=self.amount,
                refund_amount=refund_amount,
                refund_reason=reason,
                transaction_reference=transaction_reference,
            )
        )

    def is_expired(self) -> bool:
        """Check if payment has expired."""
        if not self.expires_at:
            return False
        return datetime.now(timezone.utc) > self.expires_at

    def can_be_processed(self) -> bool:
        """Check if payment can be processed."""
        return self.status == PaymentStatus.PENDING and not self.is_expired()

    def can_be_completed(self) -> bool:
        """Check if payment can be completed."""
        return self.status == PaymentStatus.PROCESSING

    def can_be_cancelled(self) -> bool:
        """Check if payment can be cancelled."""
        return self.status in [PaymentStatus.PENDING, PaymentStatus.PROCESSING]

    def can_be_refunded(self) -> bool:
        """Check if payment can be refunded."""
        return (
            self.status in [PaymentStatus.COMPLETED, PaymentStatus.PARTIALLY_REFUNDED]
            and self._is_within_refund_window()
        )

    def get_remaining_refundable_amount(self) -> Money:
        """Get the amount that can still be refunded."""
        if not self.can_be_refunded():
            return Money.zero(self.amount.currency)

        return self.amount.subtract(self.refunded_amount)

    def is_fully_refunded(self) -> bool:
        """Check if payment is fully refunded."""
        return self.refunded_amount.is_greater_than_or_equal(self.amount)

    def get_net_amount(self) -> Money:
        """Get net amount after refunds."""
        return self.amount.subtract(self.refunded_amount)

    def _add_event(self, event: DomainEvent) -> None:
        if event.aggregate_id != self.id.value:
            event = event.model_copy(update={"aggregate_id": self.id.value})
        self._events.append(event)

    def _validate_payment_invariants(self) -> None:
        """Validate business invariants for the payment."""
        if not self.amount.is_positive():
            raise InvalidPaymentAmountException(self.amount.to_float())

        if self.refunded_amount.is_greater_than(self.amount):
            raise ValueError("Refunded amount cannot exceed original payment amount")

        if self.completed_at and self.completed_at < self.created_at:
            raise ValueError("Completion time cannot be before creation time")

        if self.refunded_at and self.refunded_at < self.created_at:
            raise ValueError("Refund time cannot be before creation time")

    def _is_valid_refund_amount(self, refund_amount: Money) -> bool:
        """Validate refund amount business rules."""
        if refund_amount.currency != self.amount.currency:
            return False

        if refund_amount.to_float() < self.MIN_REFUND_AMOUNT:
            return False

        total_refund = self.refunded_amount.add(refund_amount)
        return not total_refund.is_greater_than(self.amount)

    def _is_within_refund_window(self) -> bool:
        """Check if payment is within the refund window (including cinema show rules)."""
        if not self.completed_at:
            return False

        now = datetime.now(timezone.utc)

        completed = self.completed_at
        completed_utc = (
            completed.replace(tzinfo=timezone.utc)
            if completed.tzinfo is None
            else completed.astimezone(timezone.utc)
        )

        if self.payment_type == PaymentType.TICKET_PURCHASE and self.metadata:
            show_starts = self.metadata.show_starts_at
            if show_starts is not None:
                show_utc = (
                    show_starts.replace(tzinfo=timezone.utc)
                    if show_starts.tzinfo is None
                    else show_starts.astimezone(timezone.utc)
                )
                if now >= show_utc:
                    return False

        refund_deadline = completed_utc + timedelta(days=self.MAX_PARTIAL_REFUND_DAYS)
        return now <= refund_deadline

    def __str__(self) -> str:
        return f"Payment({self.id}, {self.amount}, {self.status.value})"

    def __repr__(self) -> str:
        return (
            f"Payment(id={self.id}, user_id={self.user_id}, "
            f"amount={self.amount}, status={self.status}, "
            f"type={self.payment_type})"
        )
