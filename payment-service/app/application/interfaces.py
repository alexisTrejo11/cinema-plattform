"""
Application Layer Interfaces

Defines contracts for application services, event publishers, and external dependencies.
"""

from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional
from uuid import UUID

from app.domain.events import DomainEvent
from app.domain.entities.payment import Payment
from app.domain.entities.wallet import Wallet
from app.domain.entities.transaction import Transaction
from app.domain.value_objects import PaymentId, WalletId, TransactionId, UserId


class EventPublisher(ABC):
    """Interface for publishing domain events."""
    
    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        """Publish a single domain event."""
        pass
    
    @abstractmethod
    async def publish_batch(self, events: List[DomainEvent]) -> None:
        """Publish multiple domain events."""
        pass


class PaymentGateway(ABC):
    """Interface for external payment processing."""
    
    @abstractmethod
    async def process_payment(
        self, 
        amount: float, 
        currency: str, 
        payment_method: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process payment through external gateway."""
        pass
    
    @abstractmethod
    async def refund_payment(
        self, 
        transaction_id: str, 
        amount: float, 
        reason: str
    ) -> Dict[str, Any]:
        """Process refund through external gateway."""
        pass


class NotificationService(ABC):
    """Interface for sending notifications."""
    
    @abstractmethod
    async def send_payment_confirmation(
        self, 
        user_id: UUID, 
        payment_details: Dict[str, Any]
    ) -> None:
        """Send payment confirmation notification."""
        pass
    
    @abstractmethod
    async def send_payment_failure(
        self, 
        user_id: UUID, 
        failure_details: Dict[str, Any]
    ) -> None:
        """Send payment failure notification."""
        pass


class WalletRepository(ABC):
    """Repository interface for wallet operations."""
    
    @abstractmethod
    async def get_by_id(self, wallet_id: WalletId) -> Optional[Wallet]:
        """Get wallet by ID."""
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: UserId) -> Optional[Wallet]:
        """Get wallet by user ID."""
        pass
    
    @abstractmethod
    async def save(self, wallet: Wallet) -> Wallet:
        """Save wallet."""
        pass


class TransactionRepository(ABC):
    """Repository interface for transaction operations."""
    
    @abstractmethod
    async def get_by_id(self, transaction_id: TransactionId) -> Optional[Transaction]:
        """Get transaction by ID."""
        pass
    
    @abstractmethod
    async def get_by_wallet_id(
        self, 
        wallet_id: WalletId, 
        limit: int = 50, 
        offset: int = 0
    ) -> List[Transaction]:
        """Get transactions for a wallet."""
        pass
    
    @abstractmethod
    async def save(self, transaction: Transaction) -> Transaction:
        """Save transaction."""
        pass
