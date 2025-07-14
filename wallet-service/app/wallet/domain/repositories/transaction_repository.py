from abc import ABC, abstractmethod
from typing import List
from uuid import UUID  # Use UUID directly for transaction_id
from app.wallet.domain.entities.wallet_transaction import (
    WalletTransaction,
)


class WalletTransactionRepository(ABC):
    """Abstract base class for Wallet Transaction Repository."""

    @abstractmethod
    async def search(self, **kwargs) -> List[WalletTransaction]:
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
