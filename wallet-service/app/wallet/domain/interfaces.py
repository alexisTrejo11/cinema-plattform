from abc import ABC, abstractmethod
from typing import List, Optional
from enum import Enum
from uuid import UUID

from app.wallet.domain.entities import User, Wallet, WalletTransaction
from app.wallet.domain.value_objects import WalletId, UserId
from app.wallet.application.queries import (
    TransactionByWalletQuery,
    SearchTransactionQuery,
)


class WalletRepository(ABC):
    """Abstract repository for wallet data access."""

    @abstractmethod
    async def get_by_id(
        self,
        wallet_id: WalletId,
        raise_exception: bool = False,
    ) -> Wallet:
        """Get all wallets for a specific user asynchronously.

        Args:
            user_id: The UUID of the user whose wallets to retrieve

        Returns:
            List of Wallet objects
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id(
        self,
        user_id: UserId,
        raise_exception: bool = False,
    ) -> Wallet:
        """Retrieves all wallets for a given user."""
        raise NotImplementedError

    @abstractmethod
    async def create(self, wallet: Wallet) -> Wallet:
        """Create a new wallet asynchronously.

        Args:
            wallet: The Wallet object to create

        Returns:
            The created Wallet
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, wallet: Wallet) -> Wallet:
        """
        Update an existing wallet asynchronously.

            Args:
                wallet: The Wallet object with updated values

            Returns:
                The updated Wallet if found, None otherwise
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, wallet_id: WalletId) -> bool:
        """Delete a wallet asynchronously.

        Args:
            wallet_id: The UUID of the wallet to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        raise NotImplementedError


class WalletTransactionRepository(ABC):
    """Abstract base class for Wallet Transaction Repository."""

    @abstractmethod
    async def search(self, query: SearchTransactionQuery) -> List[WalletTransaction]:
        """
        Searches for transactions based on various criteria, with pagination and sorting.

        :param query: An instance of SearchTransactionQuery containing all filter,
                      pagination, and sorting parameters.
        :return: A list of Transaction domain objects matching the criteria.
        """
        raise NotImplementedError

    @abstractmethod
    async def list_by_wallet_id(
        self, query: TransactionByWalletQuery
    ) -> List[WalletTransaction]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, transaction: WalletTransaction) -> WalletTransaction:
        """
        Creates a new wallet transaction.

        Args:
            transaction: The WalletTransaction domain object to create.

        Returns:
            The created WalletTransaction domain object, possibly with updated properties (e.g., ID if not set).
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, transaction_id: UUID) -> bool:
        """
        Deletes a wallet transaction by its ID.

        Args:
            transaction_id: The UUID of the transaction to delete.

        Returns:
            True if the transaction was deleted successfully, False otherwise.
        """
        raise NotImplementedError


class UserInternalService(ABC):
    """Abstract service for user internal operations. Will call to user service to get user details."""

    @abstractmethod
    async def get_user_details(self, user_id: UserId) -> Optional[User]:
        """Resolve a user from the local `users` table or upstream user service."""
        raise NotImplementedError


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
