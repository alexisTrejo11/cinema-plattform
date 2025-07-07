"""
Transaction Domain Entity

Represents individual wallet transactions providing audit trail
and transaction history for financial operations.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..value_objects import (
    TransactionId, WalletId, UserId, Money, TransactionType
)
from ..exceptions import InvalidTransactionStateException


@dataclass
class Transaction:
    """
    Transaction entity representing a single wallet operation.
    
    Provides immutable record of financial transactions with
    complete audit trail information.
    """
    
    # Identity
    id: TransactionId
    wallet_id: WalletId
    user_id: UserId
    
    # Transaction details
    amount: Money
    transaction_type: TransactionType
    description: str
    
    # Timestamps
    created_at: datetime
    processed_at: Optional[datetime] = None
    
    # References and metadata
    reference_id: Optional[str] = None  # External reference (payment ID, etc.)
    related_transaction_id: Optional[TransactionId] = None  # For refunds/reversals
    
    # Balance tracking
    balance_before: Optional[Money] = None
    balance_after: Optional[Money] = None
    
    # Status and flags
    is_reversed: bool = False
    reversal_reason: Optional[str] = None
    reversed_at: Optional[datetime] = None
    
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
        balance_after: Optional[Money] = None
    ) -> Transaction:
        """
        Factory method to create a new transaction.
        
        Args:
            wallet_id: Wallet this transaction belongs to
            user_id: User who owns the wallet
            amount: Transaction amount
            transaction_type: Type of transaction
            description: Human-readable description
            reference_id: External reference
            balance_before: Wallet balance before transaction
            balance_after: Wallet balance after transaction
            
        Returns:
            New Transaction instance
        """
        transaction_id = TransactionId.generate()
        now = datetime.utcnow()
        
        return cls(
            id=transaction_id,
            wallet_id=wallet_id,
            user_id=user_id,
            amount=amount,
            transaction_type=transaction_type,
            description=description,
            created_at=now,
            processed_at=now,
            reference_id=reference_id,
            balance_before=balance_before,
            balance_after=balance_after
        )
    
    def reverse(
        self,
        reason: str,
        reversal_transaction: Optional[Transaction] = None
    ) -> None:
        """
        Mark this transaction as reversed.
        
        Args:
            reason: Reason for reversal
            reversal_transaction: The transaction that reverses this one
            
        Raises:
            InvalidTransactionStateException: If transaction is already reversed
        """
        if self.is_reversed:
            raise InvalidTransactionStateException(
                "active", "reversed"
            )
        
        self.is_reversed = True
        self.reversal_reason = reason
        self.reversed_at = datetime.utcnow()
        
        if reversal_transaction:
            self.related_transaction_id = reversal_transaction.id
    
    def can_be_reversed(self) -> bool:
        """
        Check if transaction can be reversed.
        
        Returns:
            True if transaction can be reversed, False otherwise
        """
        return (
            not self.is_reversed and
            self.transaction_type in [
                TransactionType.CREDIT,
                TransactionType.DEBIT,
                TransactionType.TRANSFER
            ]
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
            Balance change or None if balance info not available
        """
        if not self.balance_before or not self.balance_after:
            return None
        
        return self.balance_after.subtract(self.balance_before)
    
    def has_reference(self) -> bool:
        """Check if transaction has an external reference."""
        return self.reference_id is not None
    
    def is_related_to(self, other_transaction: Transaction) -> bool:
        """
        Check if this transaction is related to another.
        
        Args:
            other_transaction: Transaction to check relationship with
            
        Returns:
            True if transactions are related, False otherwise
        """
        return (
            self.related_transaction_id == other_transaction.id or
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
