from typing import Optional, List
from uuid import UUID
from app.wallet.domain.repositories.wallet_repository import WalletRepository
from ..dtos.wallet_dtos import WalletResponse


class GetWalletByIdUseCase:
    """Use case for retrieving a wallet by its ID."""

    def __init__(self, wallet_repo: WalletRepository):
        self.wallet_repo = wallet_repo

    async def execute(
        self, wallet_id: UUID, include_transactions: bool = True
    ) -> Optional[WalletResponse]:
        """Retrieves a wallet by its ID."""
        wallet = await self.wallet_repo.get_by_id(wallet_id, include_transactions)
        return WalletResponse.model_validate(wallet) if wallet else None


class GetWalletsByUserIdUseCase:
    """Use case for retrieving all wallets for a given user."""

    def __init__(self, wallet_repo: WalletRepository):
        self.wallet_repo = wallet_repo

    async def execute(
        self, user_id: UUID, include_transactions: bool = True
    ) -> List[WalletResponse]:
        """Retrieves all wallets for a given user."""
        wallets = await self.wallet_repo.get_by_user_id(user_id, include_transactions)
        return [WalletResponse.model_validate(wallet) for wallet in wallets]
