from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from app.wallet.domain.entities.wallet import Wallet


class WalletRepository(ABC):
    """Abstract repository for wallet data access."""

    @abstractmethod
    async def get_by_id(
        self, wallet_id: UUID, include_transactions: bool = False, raise_exception: bool = False
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
        self, user_id: UUID, include_transactions=False, raise_exception=False
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
    async def delete(self, wallet_id: UUID) -> bool:
        """Delete a wallet asynchronously.

        Args:
            wallet_id: The UUID of the wallet to delete

        Returns:
            True if deletion was successful, False otherwise
        """
