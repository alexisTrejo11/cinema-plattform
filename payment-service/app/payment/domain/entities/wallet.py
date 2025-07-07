"""
Wallet Domain Entity

Represents a user's wallet for storing and managing credit balances.
Handles credit/debit operations with business rules enforcement.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from ..value_objects import (
    WalletId, UserId, Money, Currency, WalletStatus, TransactionId, TransactionType
)
from ..events import (
    DomainEvent, WalletCredited, WalletDebited, InsufficientFundsDetected,
    TransactionRecorded
)
from ..exceptions import (
    InsufficientFundsException, WalletNotActiveException,
    InvalidWalletOperationException
)


@dataclass
class Wallet:
    """
    Wallet aggregate root representing a user's payment wallet.
    
    Manages credit balance and transaction history with proper
    business rule enforcement and event generation.
    """
    
    # Identity
    id: WalletId
    user_id: UserId
    
    # Balance and currency
    balance: Money
    currency: Currency
    
    # Status and metadata
    status: WalletStatus
    created_at: datetime
    updated_at: datetime
    last_transaction_at: Optional[datetime] = None
    
    # Limits and constraints
    daily_limit: Optional[Money] = None
    monthly_limit: Optional[Money] = None
    minimum_balance: Money = field(default=None)
    
    # Domain events
    _events: List[DomainEvent] = field(default_factory=list, init=False)
    
    # Business constants
    MIN_CREDIT_AMOUNT = 0.01
    MIN_DEBIT_AMOUNT = 0.01
    MAX_BALANCE_LIMIT = 10000.00  # Default maximum balance
    
    def __post_init__(self):
        """Initialize derived fields and validate business rules."""
        if self.minimum_balance is None:
            object.__setattr__(self, 'minimum_balance', Money.zero(self.currency))
        
        self._validate_wallet_invariants()
    
    @classmethod
    def create(
        cls,
        user_id: UserId,
        currency: Currency = Currency.USD,
        initial_balance: Optional[Money] = None
    ) -> Wallet:
        """
        Factory method to create a new wallet.
        
        Args:
            user_id: Owner of the wallet
            currency: Wallet currency
            initial_balance: Starting balance (default: zero)
            
        Returns:
            New Wallet instance
        """
        wallet_id = WalletId.generate()
        now = datetime.utcnow()
        
        if initial_balance is None:
            initial_balance = Money.zero(currency)
        
        wallet = cls(
            id=wallet_id,
            user_id=user_id,
            balance=initial_balance,
            currency=currency,
            status=WalletStatus.ACTIVE,
            created_at=now,
            updated_at=now,
            minimum_balance=Money.zero(currency)
        )
        
        return wallet
    
    def credit(
        self,
        amount: Money,
        description: str,
        reference_id: Optional[str] = None
    ) -> TransactionId:
        """
        Add credit to the wallet.
        
        Args:
            amount: Amount to credit
            description: Transaction description
            reference_id: External reference (e.g., payment ID)
            
        Returns:
            Transaction ID for the credit operation
            
        Raises:
            WalletNotActiveException: If wallet is not active
            InvalidWalletOperationException: If credit violates business rules
        """
        self._ensure_wallet_is_active()
        self._validate_credit_amount(amount)
        
        # Check daily/monthly limits if configured
        if self.daily_limit:
            # In a real implementation, you'd check daily transaction totals
            pass
        
        if self.monthly_limit:
            # In a real implementation, you'd check monthly transaction totals
            pass
        
        # Check maximum balance limit
        new_balance = self.balance.add(amount)
        if new_balance.to_float() > self.MAX_BALANCE_LIMIT:
            raise InvalidWalletOperationException(
                "credit",
                f"Would exceed maximum balance limit of {self.MAX_BALANCE_LIMIT}"
            )
        
        # Apply the credit
        previous_balance = self.balance
        self.balance = new_balance
        self.updated_at = datetime.utcnow()
        self.last_transaction_at = self.updated_at
        
        # Generate transaction ID and record the transaction
        transaction_id = TransactionId.generate()
        
        # Raise domain events
        self._add_event(WalletCredited(
            wallet_id=self.id,
            user_id=self.user_id,
            amount=amount,
            previous_balance=previous_balance,
            new_balance=self.balance,
            transaction_id=transaction_id,
            description=description
        ))
        
        self._add_event(TransactionRecorded(
            transaction_id=transaction_id,
            wallet_id=self.id,
            user_id=self.user_id,
            amount=amount,
            transaction_type=TransactionType.CREDIT,
            description=description,
            reference_id=reference_id
        ))
        
        return transaction_id
    
    def debit(
        self,
        amount: Money,
        description: str,
        reference_id: Optional[str] = None,
        allow_overdraft: bool = False
    ) -> TransactionId:
        """
        Debit amount from the wallet.
        
        Args:
            amount: Amount to debit
            description: Transaction description
            reference_id: External reference (e.g., payment ID)
            allow_overdraft: Whether to allow negative balance
            
        Returns:
            Transaction ID for the debit operation
            
        Raises:
            WalletNotActiveException: If wallet is not active
            InsufficientFundsException: If insufficient funds
            InvalidWalletOperationException: If debit violates business rules
        """
        self._ensure_wallet_is_active()
        self._validate_debit_amount(amount)
        
        # Check if sufficient funds available
        if not allow_overdraft:
            required_balance = self.minimum_balance.add(amount)
            if not self.balance.is_greater_than_or_equal(required_balance):
                transaction_id = TransactionId.generate()
                self._add_event(InsufficientFundsDetected(
                    wallet_id=self.id,
                    user_id=self.user_id,
                    required_amount=amount,
                    available_balance=self.balance,
                    attempted_transaction_id=transaction_id
                ))
                raise InsufficientFundsException(
                    self.balance.to_float(),
                    amount.to_float()
                )
        
        # Apply the debit
        previous_balance = self.balance
        self.balance = previous_balance.subtract(amount)
        self.updated_at = datetime.utcnow()
        self.last_transaction_at = self.updated_at
        
        # Generate transaction ID and record the transaction
        transaction_id = TransactionId.generate()
        
        # Raise domain events
        self._add_event(WalletDebited(
            wallet_id=self.id,
            user_id=self.user_id,
            amount=amount,
            previous_balance=previous_balance,
            new_balance=self.balance,
            transaction_id=transaction_id,
            description=description
        ))
        
        self._add_event(TransactionRecorded(
            transaction_id=transaction_id,
            wallet_id=self.id,
            user_id=self.user_id,
            amount=amount,
            transaction_type=TransactionType.DEBIT,
            description=description,
            reference_id=reference_id
        ))
        
        return transaction_id
    
    def can_debit(self, amount: Money) -> bool:
        """
        Check if wallet has sufficient funds for debit.
        
        Args:
            amount: Amount to check
            
        Returns:
            True if debit is possible, False otherwise
        """
        if not self.is_active():
            return False
        
        if amount.currency != self.currency:
            return False
        
        required_balance = self.minimum_balance.add(amount)
        return self.balance.is_greater_than_or_equal(required_balance)
    
    def get_available_balance(self) -> Money:
        """
        Get available balance for spending.
        
        Returns:
            Available balance after considering minimum balance
        """
        if self.balance.is_greater_than(self.minimum_balance):
            return self.balance.subtract(self.minimum_balance)
        return Money.zero(self.currency)
    
    def suspend(self, reason: str) -> None:
        """
        Suspend the wallet.
        
        Args:
            reason: Reason for suspension
        """
        if self.status == WalletStatus.CLOSED:
            raise InvalidWalletOperationException(
                "suspend",
                "Cannot suspend a closed wallet"
            )
        
        self.status = WalletStatus.SUSPENDED
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Activate a suspended wallet."""
        if self.status == WalletStatus.CLOSED:
            raise InvalidWalletOperationException(
                "activate",
                "Cannot activate a closed wallet"
            )
        
        self.status = WalletStatus.ACTIVE
        self.updated_at = datetime.utcnow()
    
    def freeze(self, reason: str) -> None:
        """
        Freeze the wallet temporarily.
        
        Args:
            reason: Reason for freezing
        """
        if self.status == WalletStatus.CLOSED:
            raise InvalidWalletOperationException(
                "freeze",
                "Cannot freeze a closed wallet"
            )
        
        self.status = WalletStatus.FROZEN
        self.updated_at = datetime.utcnow()
    
    def close(self, reason: str) -> None:
        """
        Permanently close the wallet.
        
        Args:
            reason: Reason for closure
            
        Raises:
            InvalidWalletOperationException: If wallet has remaining balance
        """
        if not self.balance.is_zero():
            raise InvalidWalletOperationException(
                "close",
                f"Cannot close wallet with remaining balance: {self.balance}"
            )
        
        self.status = WalletStatus.CLOSED
        self.updated_at = datetime.utcnow()
    
    def is_active(self) -> bool:
        """Check if wallet is active."""
        return self.status == WalletStatus.ACTIVE
    
    def is_usable(self) -> bool:
        """Check if wallet can be used for transactions."""
        return self.status in [WalletStatus.ACTIVE]
    
    def set_daily_limit(self, limit: Money) -> None:
        """Set daily transaction limit."""
        if limit.currency != self.currency:
            raise ValueError("Limit currency must match wallet currency")
        
        self.daily_limit = limit
        self.updated_at = datetime.utcnow()
    
    def set_monthly_limit(self, limit: Money) -> None:
        """Set monthly transaction limit."""
        if limit.currency != self.currency:
            raise ValueError("Limit currency must match wallet currency")
        
        self.monthly_limit = limit
        self.updated_at = datetime.utcnow()
    
    def get_events(self) -> List[DomainEvent]:
        """Get domain events generated by this aggregate."""
        return self._events.copy()
    
    def clear_events(self) -> None:
        """Clear domain events after publishing."""
        self._events.clear()
    
    def _add_event(self, event: DomainEvent) -> None:
        """Add a domain event to the aggregate."""
        event.aggregate_id = self.id.value
        self._events.append(event)
    
    def _ensure_wallet_is_active(self) -> None:
        """Ensure wallet is in a usable state."""
        if not self.is_usable():
            raise WalletNotActiveException(str(self.id))
    
    def _validate_credit_amount(self, amount: Money) -> None:
        """Validate credit amount business rules."""
        if amount.currency != self.currency:
            raise InvalidWalletOperationException(
                "credit",
                f"Currency mismatch: wallet={self.currency}, amount={amount.currency}"
            )
        
        if amount.to_float() < self.MIN_CREDIT_AMOUNT:
            raise InvalidWalletOperationException(
                "credit",
                f"Amount below minimum: {amount.to_float()} < {self.MIN_CREDIT_AMOUNT}"
            )
    
    def _validate_debit_amount(self, amount: Money) -> None:
        """Validate debit amount business rules."""
        if amount.currency != self.currency:
            raise InvalidWalletOperationException(
                "debit",
                f"Currency mismatch: wallet={self.currency}, amount={amount.currency}"
            )
        
        if amount.to_float() < self.MIN_DEBIT_AMOUNT:
            raise InvalidWalletOperationException(
                "debit",
                f"Amount below minimum: {amount.to_float()} < {self.MIN_DEBIT_AMOUNT}"
            )
    
    def _validate_wallet_invariants(self) -> None:
        """Validate business invariants for the wallet."""
        # Balance currency must match wallet currency
        if self.balance.currency != self.currency:
            raise ValueError("Balance currency must match wallet currency")
        
        # Minimum balance must be non-negative
        if self.minimum_balance.to_float() < 0:
            raise ValueError("Minimum balance cannot be negative")
        
        # Limits must be positive if set
        if self.daily_limit and not self.daily_limit.is_positive():
            raise ValueError("Daily limit must be positive")
        
        if self.monthly_limit and not self.monthly_limit.is_positive():
            raise ValueError("Monthly limit must be positive")
    
    def __str__(self) -> str:
        return f"Wallet({self.id}, {self.balance}, {self.status.value})"
    
    def __repr__(self) -> str:
        return (
            f"Wallet(id={self.id}, user_id={self.user_id}, "
            f"balance={self.balance}, status={self.status})"
        )
