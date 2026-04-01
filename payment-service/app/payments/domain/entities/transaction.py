"""
Transaction Domain Entity

Represents individual wallet transactions providing audit trail
and transaction history for financial operations.
"""

from datetime import datetime, timezone
from typing import Optional

from pydantic import ConfigDict

from ..aggregate_root import AggregateRoot
from ..events import DomainEvent, TransactionReversed
from ..value_objects import (
    TransactionId,
    WalletId,
    UserId,
    Money,
    TransactionType,
)
from ..exceptions import InvalidTransactionStateException


class Transaction(AggregateRoot):
    """
    Transaction entity representing a single operation.

    Provides immutable record of financial transactions with
    complete audit trail information.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=False)

    id: TransactionId
    wallet_id: WalletId
    user_id: UserId

    amount: Money
    transaction_type: TransactionType
    description: str

    created_at: datetime
    processed_at: Optional[datetime] = None

    reference_id: Optional[str] = None  # Generic external reference
    stripe_payment_intent_id: Optional[str] = None  # Stripe pi_xxx when applicable
    stripe_event_id: Optional[str] = None  # Stripe webhook evt_xxx when applicable
    related_transaction_id: Optional[TransactionId] = None  # For refunds/reversals

    balance_before: Optional[Money] = None
    balance_after: Optional[Money] = None

    is_reversed: bool = False
    reversal_reason: Optional[str] = None
    reversed_at: Optional[datetime] = None

    def _add_event(self, event: DomainEvent) -> None:
        if event.aggregate_id != self.id.value:
            event = event.model_copy(update={"aggregate_id": self.id.value})
        self._events.append(event)

    @classmethod
    def create(
        cls,
        wallet_id: WalletId,
        user_id: UserId,
        amount: Money,
        transaction_type: TransactionType,
        description: str,
        reference_id: Optional[str] = None,
        balance_before: Optional[Money] = None,
        balance_after: Optional[Money] = None,
        stripe_payment_intent_id: Optional[str] = None,
        stripe_event_id: Optional[str] = None,
    ) -> Transaction:
        """
        Factory method to create a new transaction.

        ``processed_at`` is left unset until the transaction is confirmed processed;
        call ``mark_processed`` when the wallet or gateway confirms settlement.
        """
        transaction_id = TransactionId.generate()
        now = datetime.now(timezone.utc)

        return cls(
            id=transaction_id,
            wallet_id=wallet_id,
            user_id=user_id,
            amount=amount,
            transaction_type=transaction_type,
            description=description,
            created_at=now,
            processed_at=None,
            reference_id=reference_id,
            stripe_payment_intent_id=stripe_payment_intent_id,
            stripe_event_id=stripe_event_id,
            balance_before=balance_before,
            balance_after=balance_after,
        )

    def mark_processed(self, at: Optional[datetime] = None) -> None:
        """Record when this transaction was confirmed processed (wallet settled, etc.)."""
        self.processed_at = at or datetime.now(timezone.utc)

    def reverse(
        self,
        reason: str,
        reversal_transaction: Optional[Transaction] = None,
    ) -> None:
        """
        Mark this transaction as reversed.

        Raises:
            InvalidTransactionStateException: If transaction is already reversed
        """
        if self.is_reversed:
            raise InvalidTransactionStateException("active", "reversed")

        self.is_reversed = True
        self.reversal_reason = reason
        self.reversed_at = datetime.now(timezone.utc)

        if reversal_transaction:
            self.related_transaction_id = reversal_transaction.id

        self._add_event(
            TransactionReversed(
                transaction_id=self.id,
                wallet_id=self.wallet_id,
                user_id=self.user_id,
                amount=self.amount,
                transaction_type=self.transaction_type,
                reversal_reason=reason,
            )
        )

    def can_be_reversed(self) -> bool:
        """
        Whether this transaction may be reversed.

        Includes CREDIT, DEBIT, TRANSFER, and REFUND so an erroneous refund can be
        corrected via a compensating reversal; adjust if your policy forbids reversing REFUND.
        """
        return not self.is_reversed and self.transaction_type in (
            TransactionType.CREDIT,
            TransactionType.DEBIT,
            TransactionType.TRANSFER,
            TransactionType.REFUND,
        )

    def is_credit(self) -> bool:
        """Check if this is a credit transaction."""
        return self.transaction_type == TransactionType.CREDIT

    def is_debit(self) -> bool:
        """Check if this is a debit transaction."""
        return self.transaction_type == TransactionType.DEBIT

    def is_refund(self) -> bool:
        """Check if this is a refund transaction."""
        return self.transaction_type == TransactionType.REFUND

    def is_transfer(self) -> bool:
        """Check if this is a transfer transaction."""
        return self.transaction_type == TransactionType.TRANSFER

    def is_fee(self) -> bool:
        """Check if this is a fee transaction."""
        return self.transaction_type == TransactionType.FEE

    def get_effective_amount(self) -> Money:
        """
        Get the effective amount considering reversal status.

        Returns:
            Zero if reversed, otherwise the original amount
        """
        if self.is_reversed:
            return Money.zero(self.amount.currency)
        return self.amount

    def get_balance_change(self) -> Optional[Money]:
        """
        Calculate the balance change from this transaction.

        Returns:
            Balance change, or None if balance info is missing or currencies mismatch.
        """
        if not self.balance_before or not self.balance_after:
            return None
        if self.balance_before.currency != self.balance_after.currency:
            return None
        return self.balance_after.subtract(self.balance_before)

    def has_reference(self) -> bool:
        """Check if transaction has an external reference."""
        return self.reference_id is not None

    def is_related_to(self, other_transaction: Transaction) -> bool:
        """
        Check if this transaction is related to another.
        """
        return self.related_transaction_id == other_transaction.id or (
            other_transaction.related_transaction_id == self.id
        )

    def __str__(self) -> str:
        status = "REVERSED" if self.is_reversed else "ACTIVE"
        return f"Transaction({self.id}, {self.amount}, {self.transaction_type.value}, {status})"

    def __repr__(self) -> str:
        return (
            f"Transaction(id={self.id}, wallet_id={self.wallet_id}, "
            f"amount={self.amount}, type={self.transaction_type}, "
            f"reversed={self.is_reversed})"
        )
