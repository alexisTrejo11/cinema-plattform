from app.wallet.domain.repositories.wallet_repository import WalletRepository
from app.wallet.presentation.dtos.response import WalletResponse
from ...query.queries import GetWalletByIdQuery, GetWalletByUserIdQuery


class GetWalletByIdUseCase:
    """Use case for retrieving a wallet by its ID."""

    def __init__(self, wallet_repo: WalletRepository):
        self.wallet_repo = wallet_repo

    async def execute(self, query: GetWalletByIdQuery) -> WalletResponse:
        """Retrieves a wallet by its ID."""
        wallet = await self.wallet_repo.get_by_id(
            wallet_id=query.walletId,
            raise_exception=True,
            transaction_query=(query.model_dump()),
        )

        return WalletResponse.from_domain(wallet)


class GetWalletsByUserIdUseCase:
    """Use case for retrieving all wallets for a given user."""

    def __init__(self, wallet_repo: WalletRepository):
        self.wallet_repo = wallet_repo

    async def execute(self, query: GetWalletByUserIdQuery) -> WalletResponse:
        """Retrieves all wallets for a given user."""
        wallet = await self.wallet_repo.get_by_user_id(
            user_id=query.userId,
            transaction_query=query.model_dump(),
            raise_exception=True,
        )

        return WalletResponse.from_domain(wallet)
