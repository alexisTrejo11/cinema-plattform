from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional, Dict, Any

from app.shared.events.base import BaseEvent
from app.payments.domain.entities import Payment, Wallet, Transaction
from app.payments.domain.value_objects import PaymentId, WalletId, TransactionId, UserId


class PaymentRepository(ABC):
    @abstractmethod
    async def get_by_id(self, payment_id: PaymentId) -> Optional[Payment]:
        """Get a payment by its ID."""
        pass

    @abstractmethod
    async def list(self, **kwargs) -> List[Payment]:
        """List payments with filters."""
        pass

    @abstractmethod
    async def save(self, payment: Payment) -> Payment:
        """Save a payment."""
        pass

    @abstractmethod
    async def delete(self, payment_id: PaymentId) -> bool:
        """Delete a payment by its ID."""
        pass


class EventPublisher(ABC):
    """Interface for publishing domain events."""

    @abstractmethod
    async def publish(self, event: BaseEvent) -> None:
        """Publish a single domain event."""
        pass

    @abstractmethod
    async def publish_batch(self, events: List[BaseEvent]) -> None:
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
        metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Process payment through external gateway."""
        pass

    @abstractmethod
    async def refund_payment(
        self, transaction_id: str, amount: float, reason: str
    ) -> Dict[str, Any]:
        """Process refund through external gateway."""
        pass


class NotificationService(ABC):
    """Interface for sending notifications."""

    @abstractmethod
    async def send_payment_confirmation(
        self, user_id: UUID, payment_details: Dict[str, Any]
    ) -> None:
        """Send payment confirmation notification."""
        pass

    @abstractmethod
    async def send_payment_failure(
        self, user_id: UUID, failure_details: Dict[str, Any]
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
        self, wallet_id: WalletId, limit: int = 50, offset: int = 0
    ) -> List[Transaction]:
        """Get transactions for a wallet."""
        pass

    @abstractmethod
    async def save(self, transaction: Transaction) -> Transaction:
        """Save transaction."""
        pass
