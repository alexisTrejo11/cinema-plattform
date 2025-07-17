from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from app.wallet.domain.entities.wallet_transaction import (
    WalletTransaction,
)
from app.wallet.application.query.queries import (
    TransactionByWalletQuery,
    SearchTransactionQuery,
)


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
