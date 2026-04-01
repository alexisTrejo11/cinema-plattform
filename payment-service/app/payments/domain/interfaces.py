from abc import ABC, abstractmethod
from uuid import UUID
from typing import Any, Dict, List, Optional

from app.payments.domain.entities import Payment, StoredPaymentMethod, Transaction, PaymentMethod
from app.payments.domain.payment_list_criteria import PaymentListCriteria
from app.payments.domain.value_objects import PaymentId, WalletId, TransactionId, UserId


class PaymentRepository(ABC):
    @abstractmethod
    async def get_by_id(self, payment_id: PaymentId) -> Optional[Payment]:
        """Get a payment by its ID."""
        pass

    @abstractmethod
    async def list(self, criteria: PaymentListCriteria) -> List[Payment]:
        """List payments with filters and pagination."""
        pass

    @abstractmethod
    async def save(self, payment: Payment) -> Payment:
        """Save a payment."""
        pass

    @abstractmethod
    async def delete(self, payment_id: PaymentId) -> bool:
        """Delete a payment by its ID."""
        pass


class PurchaseAssertionClient(ABC):
    """
    Sync boundary for cross-service business assertions (gRPC in production).

    For now this is an abstract port; infrastructure can provide a no-op adapter
    until the real remote calls are implemented.
    """

    @abstractmethod
    async def assert_ticket_purchase(
        self, user_id: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def assert_concessions_purchase(
        self, user_id: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def assert_merchandise_purchase(
        self, user_id: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def assert_subscription_purchase(
        self, user_id: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def assert_wallet_credit(
        self, user_id: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass


class PaymentEventsPublisher(ABC):
    """Application-level publisher for integration events (Kafka later)."""

    @abstractmethod
    async def publish(
        self, event_name: str, payload: Dict[str, Any], key: str | None = None
    ) -> None:
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


class WalletRepository(ABC):
    """Repository interface for wallet operations."""

    @abstractmethod
    async def get_by_id(self, wallet_id: WalletId) -> Optional[Any]:
        """Get wallet by ID."""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UserId) -> Optional[Any]:
        """Get wallet by user ID."""
        pass

    @abstractmethod
    async def save(self, wallet: Any) -> Any:
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


class PaymentMethodRepository(ABC):
    """Repository interface for payment methods operations."""

    @abstractmethod
    async def find_all(self) -> List[PaymentMethod]:
        """Get all payment methods."""
        pass

    @abstractmethod
    async def find_by_id(
        self, payment_method_id: str, include_deleted: bool = False
    ) -> Optional[PaymentMethod]:
        """Get payment method by ID."""
        pass

    @abstractmethod
    async def save(self, payment_method: PaymentMethod) -> PaymentMethod:
        """Create or update a payment method."""
        pass

    @abstractmethod
    async def delete(self, payment_method_id: str) -> bool:
        """Delete a payment method."""
        pass


class StoredPaymentMethodRepository(ABC):
    """User-saved payment instruments (not the catalog ``PaymentMethod``)."""

    @abstractmethod
    async def save(self, stored: StoredPaymentMethod) -> StoredPaymentMethod:
        pass

    @abstractmethod
    async def get_for_user(self, stored_id: str, user_id: str) -> Optional[StoredPaymentMethod]:
        pass

    @abstractmethod
    async def list_for_user(self, user_id: str) -> List[StoredPaymentMethod]:
        pass
