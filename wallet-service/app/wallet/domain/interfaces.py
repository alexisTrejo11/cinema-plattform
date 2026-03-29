from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Tuple, Any
from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from app.shared.core.pagination import Page
from app.shared.core.response import Result
from app.wallet.domain.entities import User, Wallet, WalletTransaction
from app.wallet.domain.summary import TransactionTypeAggregateRow
from app.wallet.domain.value_objects import WalletId, UserId
from app.wallet.application.queries import (
    TransactionByWalletQuery,
    SearchTransactionQuery,
)


class WalletRepository(ABC):
    """Abstract repository for wallet data access."""

    @abstractmethod
    async def find_by_id(
        self,
        wallet_id: WalletId,
        inclue_deleted: bool = False,
    ) -> Wallet:
        """Get all wallets for a specific user asynchronously.

        Args:
            user_id: The UUID of the user whose wallets to retrieve

        Returns:
            List of Wallet objects
        """
        pass

    @abstractmethod
    async def find_by_user_id(
        self,
        user_id: UserId,
        include_deleted: bool = False,
    ) -> Wallet:
        """Retrieves all wallets for a given user."""
        pass

    @abstractmethod
    async def create(self, wallet: Wallet) -> Wallet:
        """Create a new wallet asynchronously.

        Args:
            wallet: The Wallet object to create

        Returns:
            The created Wallet
        """
        pass

    @abstractmethod
    async def update(self, wallet: Wallet) -> Wallet:
        """Update a wallet asynchronously.

        Args:
            wallet: The Wallet object to update
        """
        pass

    @abstractmethod
    async def delete(self, wallet_id: WalletId) -> bool:
        """Delete a wallet asynchronously.

        Args:
            wallet_id: The UUID of the wallet to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        pass

    @abstractmethod
    async def exists_by_user_id(self, user_id: UserId) -> bool:
        """
        Checks if a wallet exists for a given user ID.

        Args:
            user_id: The UUID of the user to check

        Returns:
            True if a wallet exists for the user, False otherwise
        """
        pass


class WalletTransactionRepository(ABC):
    """Abstract base class for Wallet Transaction Repository."""

    @abstractmethod
    async def search(self, query: SearchTransactionQuery) -> Page[WalletTransaction]:
        """
        Searches for transactions based on various criteria, with pagination and sorting.

        :param query: An instance of SearchTransactionQuery containing all filter,
                      pagination, and sorting parameters.
        :return: A list of Transaction domain objects matching the criteria.
        """
        pass

    @abstractmethod
    async def find_by_wallet_id(
        self, query: TransactionByWalletQuery
    ) -> List[WalletTransaction]:
        pass

    @abstractmethod
    async def aggregate_by_wallet_id(
        self,
        wallet_id: WalletId,
        *,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
    ) -> Tuple[int, List[TransactionTypeAggregateRow]]:
        """Total transaction count and per-type counts/sums for a wallet (optional date window)."""
        pass

    @abstractmethod
    async def create(self, transaction: WalletTransaction) -> WalletTransaction:
        """
        Creates a new wallet transaction.

        Args:
            transaction: The WalletTransaction domain object to create.

        Returns:
            The created WalletTransaction domain object, possibly with updated properties (e.g., ID if not set).
        """
        pass

    @abstractmethod
    async def delete(self, transaction_id: UUID) -> bool:
        """
        Deletes a wallet transaction by its ID.

        Args:
            transaction_id: The UUID of the transaction to delete.

        Returns:
            True if the transaction was deleted successfully, False otherwise.
        """
        pass


class UserInternalService(ABC):
    """Abstract service for user internal operations. Will call to user service to get user details."""

    @abstractmethod
    async def get_user_details(self, user_id: UserId) -> Result[User]:
        """Resolve a user from the local `users` table or upstream user service."""
        pass


class PaymentInternalService(ABC):
    """Abstract service for payment internal operations. Will call to payment service to get payment details."""

    @abstractmethod
    async def create_payment(
        self, payment_details: dict[str, Any]
    ) -> Result[dict[str, Any]]:
        """Create a and validate new payment. Return the payment details if successful."""
        pass


class PaymentDetails(BaseModel):
    """Payment details."""

    id: str
    amount: float
    currency: str
    status: str
    created_at: datetime


class TransactionEvents(Enum):
    CHARGE_CREDIT = "CHARGE_CREDIT"
    BUY_PRODUCT = "BUY_PRODUCT"


class WalletEventPublisher(ABC):
    @abstractmethod
    async def publish_event(
        self,
        user_wallet: Wallet,
        new_transaction: WalletTransaction,
        event_type: TransactionEvents,
    ):
        pass
