"""
Payment Domain Entity

Core business entity representing a payment in the cinema system.
Implements business rules and invariants for payment processing.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

from ..value_objects import (
    PaymentId, UserId, Money, PaymentMethod, PaymentStatus, 
    PaymentType, PaymentReference, PaymentMetadata, Currency
)
from ..events import (
    DomainEvent, PaymentCreated, PaymentProcessingStarted, 
    PaymentCompleted, PaymentFailed, PaymentRefunded
)
from ..exceptions import (
    PaymentAlreadyProcessedException, PaymentNotRefundableException,
    InvalidPaymentAmountException
)


@dataclass
class Payment:
    """
    Payment aggregate root representing a payment transaction.
    
    Encapsulates all business rules related to payment processing,
    status management, and refund handling.
    """
    
    # Identity
    id: PaymentId
    user_id: UserId
    
    # Payment details
    amount: Money
    payment_method: PaymentMethod
    payment_type: PaymentType
    status: PaymentStatus
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # References and metadata
    external_reference: Optional[PaymentReference] = None
    metadata: Optional[PaymentMetadata] = None
    failure_reason: Optional[str] = None
    
    # Refund information
    refunded_amount: Money = field(default=None)
    refund_reason: Optional[str] = None
    refunded_at: Optional[datetime] = None
    
    # Domain events
    _events: List[DomainEvent] = field(default_factory=list, init=False)
    
    # Business constants
    PAYMENT_EXPIRY_MINUTES = 30
    MIN_REFUND_AMOUNT = 0.01
    MAX_PARTIAL_REFUND_DAYS = 30
    
    def __post_init__(self):
        """Initialize derived fields and validate business rules."""
        if self.refunded_amount is None:
            object.__setattr__(self, 'refunded_amount', Money.zero(self.amount.currency))
        
        # Validate business invariants
        self._validate_payment_invariants()
    
    @classmethod
    def create(
        cls,
        user_id: UserId,
        amount: Money,
        payment_method: PaymentMethod,
        payment_type: PaymentType,
        metadata: Optional[PaymentMetadata] = None
    ) -> Payment:
        """
        Factory method to create a new payment.
        
        Args:
            user_id: User making the payment
            amount: Payment amount with currency
            payment_method: Method of payment
            payment_type: Type of payment (ticket, food, etc.)
            metadata: Additional payment context
            
        Returns:
            New Payment instance
            
        Raises:
            InvalidPaymentAmountException: If amount is invalid
        """
        # Business rule: Minimum payment amount
        if amount.amount <= 0:
            raise InvalidPaymentAmountException(amount.to_float())
        
        payment_id = PaymentId.generate()
        now = datetime.utcnow()
        
        payment = cls(
            id=payment_id,
            user_id=user_id,
            amount=amount,
            payment_method=payment_method,
            payment_type=payment_type,
            status=PaymentStatus.PENDING,
            created_at=now,
            updated_at=now,
            expires_at=now + timedelta(minutes=cls.PAYMENT_EXPIRY_MINUTES),
            metadata=metadata,
            refunded_amount=Money.zero(amount.currency)
        )
        
        # Raise domain event
        payment._add_event(PaymentCreated(
            payment_id=payment_id,
            user_id=user_id,
            amount=amount,
            payment_type=payment_type,
            metadata=metadata.__dict__ if metadata else None
        ))
        
        return payment
    
    def start_processing(self, external_reference: Optional[PaymentReference] = None) -> None:
        """
        Begin payment processing.
        
        Args:
            external_reference: Reference from payment gateway
            
        Raises:
            PaymentAlreadyProcessedException: If payment is not in pending status
        """
        if not self.can_be_processed():
            raise PaymentAlreadyProcessedException(str(self.id), self.status.value)
        
        self.status = PaymentStatus.PROCESSING
        self.external_reference = external_reference
        self.updated_at = datetime.utcnow()
        
        self._add_event(PaymentProcessingStarted(
            payment_id=self.id,
            user_id=self.user_id,
            amount=self.amount,
            payment_method=self.payment_method.value
        ))
    
    def complete(self, transaction_reference: Optional[str] = None) -> None:
        """
        Mark payment as completed successfully.
        
        Args:
            transaction_reference: Reference ID from payment processor
            
        Raises:
            PaymentAlreadyProcessedException: If payment cannot be completed
        """
        if not self.can_be_completed():
            raise PaymentAlreadyProcessedException(str(self.id), self.status.value)
        
        self.status = PaymentStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.updated_at = self.completed_at
        
        # Update external reference if provided
        if transaction_reference and self.external_reference:
            self.external_reference = PaymentReference(
                provider=self.external_reference.provider,
                reference_id=transaction_reference
            )
        
        self._add_event(PaymentCompleted(
            payment_id=self.id,
            user_id=self.user_id,
            amount=self.amount,
            payment_type=self.payment_type,
            transaction_reference=transaction_reference,
            metadata=self.metadata.__dict__ if self.metadata else None
        ))
    
    def fail(self, reason: str, error_code: Optional[str] = None) -> None:
        """
        Mark payment as failed.
        
        Args:
            reason: Human-readable failure reason
            error_code: Machine-readable error code
        """
        if self.status in [PaymentStatus.COMPLETED, PaymentStatus.REFUNDED]:
            raise PaymentAlreadyProcessedException(str(self.id), self.status.value)
        
        self.status = PaymentStatus.FAILED
        self.failure_reason = reason
        self.updated_at = datetime.utcnow()
        
        self._add_event(PaymentFailed(
            payment_id=self.id,
            user_id=self.user_id,
            amount=self.amount,
            failure_reason=reason,
            error_code=error_code
        ))
    
    def cancel(self, reason: str = "Cancelled by user") -> None:
        """
        Cancel a pending payment.
        
        Args:
            reason: Cancellation reason
        """
        if not self.can_be_cancelled():
            raise PaymentAlreadyProcessedException(str(self.id), self.status.value)
        
        self.status = PaymentStatus.CANCELLED
        self.failure_reason = reason
        self.updated_at = datetime.utcnow()
        
        self._add_event(PaymentFailed(
            payment_id=self.id,
            user_id=self.user_id,
            amount=self.amount,
            failure_reason=reason,
            error_code="PAYMENT_CANCELLED"
        ))
    
    def refund(
        self, 
        refund_amount: Money, 
        reason: str,
        transaction_reference: Optional[str] = None
    ) -> None:
        """
        Process a refund for this payment.
        
        Args:
            refund_amount: Amount to refund
            reason: Reason for refund
            transaction_reference: Reference from payment processor
            
        Raises:
            PaymentNotRefundableException: If payment cannot be refunded
        """
        if not self.can_be_refunded():
            raise PaymentNotRefundableException(str(self.id), "Payment is not in refundable state")
        
        if not self._is_valid_refund_amount(refund_amount):
            raise PaymentNotRefundableException(
                str(self.id), 
                f"Invalid refund amount: {refund_amount}"
            )
        
        if not self._is_within_refund_window():
            raise PaymentNotRefundableException(
                str(self.id), 
                "Refund window has expired"
            )
        
        # Update refund information
        new_refunded_amount = self.refunded_amount.add(refund_amount)
        self.refunded_amount = new_refunded_amount
        self.refund_reason = reason
        self.refunded_at = datetime.utcnow()
        self.updated_at = self.refunded_at
        
        # Update status based on refund amount
        if new_refunded_amount.is_greater_than_or_equal(self.amount):
            self.status = PaymentStatus.REFUNDED
        else:
            self.status = PaymentStatus.PARTIALLY_REFUNDED
        
        self._add_event(PaymentRefunded(
            payment_id=self.id,
            user_id=self.user_id,
            original_amount=self.amount,
            refund_amount=refund_amount,
            refund_reason=reason,
            transaction_reference=transaction_reference
        ))
    
    def is_expired(self) -> bool:
        """Check if payment has expired."""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
    
    def can_be_processed(self) -> bool:
        """Check if payment can be processed."""
        return (
            self.status == PaymentStatus.PENDING and 
            not self.is_expired()
        )
    
    def can_be_completed(self) -> bool:
        """Check if payment can be completed."""
        return self.status == PaymentStatus.PROCESSING
    
    def can_be_cancelled(self) -> bool:
        """Check if payment can be cancelled."""
        return self.status in [PaymentStatus.PENDING, PaymentStatus.PROCESSING]
    
    def can_be_refunded(self) -> bool:
        """Check if payment can be refunded."""
        return (
            self.status in [PaymentStatus.COMPLETED, PaymentStatus.PARTIALLY_REFUNDED] and
            self._is_within_refund_window()
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
    
    def get_events(self) -> List[DomainEvent]:
        """Get domain events generated by this aggregate."""
        return self._events.copy()
    
    def clear_events(self) -> None:
        """Clear domain events after publishing."""
        self._events.clear()
    
    def _add_event(self, event: DomainEvent) -> None:
        """Add a domain event to the aggregate."""
        # If the event supports aggregate_id in its constructor, recreate it with the correct aggregate_id
        if hasattr(event, 'aggregate_id') and getattr(event, 'aggregate_id', None) != self.id.value:
            # Try to recreate the event with aggregate_id if possible
            try:
                event = type(event)(**{**event.__dict__, 'aggregate_id': self.id.value})
            except TypeError:
                pass  # If not possible, just use the event as is
        self._events.append(event)
    
    def _validate_payment_invariants(self) -> None:
        """Validate business invariants for the payment."""
        # Amount must be positive
        if not self.amount.is_positive():
            raise InvalidPaymentAmountException(self.amount.to_float())
        
        # Refunded amount cannot exceed original amount
        if self.refunded_amount.is_greater_than(self.amount):
            raise ValueError("Refunded amount cannot exceed original payment amount")
        
        # Timestamps must be consistent
        if self.completed_at and self.completed_at < self.created_at:
            raise ValueError("Completion time cannot be before creation time")
        
        if self.refunded_at and self.refunded_at < self.created_at:
            raise ValueError("Refund time cannot be before creation time")
    
    def _is_valid_refund_amount(self, refund_amount: Money) -> bool:
        """Validate refund amount business rules."""
        # Currency must match
        if refund_amount.currency != self.amount.currency:
            return False
        
        # Amount must be positive and above minimum
        if refund_amount.to_float() < self.MIN_REFUND_AMOUNT:
            return False
        
        # Total refunded amount cannot exceed original amount
        total_refund = self.refunded_amount.add(refund_amount)
        return not total_refund.is_greater_than(self.amount)
    
    def _is_within_refund_window(self) -> bool:
        """Check if payment is within the refund window."""
        if not self.completed_at:
            return False
        
        # For certain payment types, allow longer refund windows
        if self.payment_type in [PaymentType.TICKET_PURCHASE]:
            # Check if event hasn't started (would need integration with show service)
            # For now, use a standard window
            pass
        
        refund_deadline = self.completed_at + timedelta(days=self.MAX_PARTIAL_REFUND_DAYS)
        return datetime.utcnow() <= refund_deadline
    
    def __str__(self) -> str:
        return f"Payment({self.id}, {self.amount}, {self.status.value})"
    
    def __repr__(self) -> str:
        return (
            f"Payment(id={self.id}, user_id={self.user_id}, "
            f"amount={self.amount}, status={self.status}, "
            f"type={self.payment_type})"
        )
