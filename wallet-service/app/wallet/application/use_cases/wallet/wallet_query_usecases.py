from app.wallet.domain.repositories.wallet_repository import WalletRepository
from app.wallet.domain.repositories.transaction_repository import (
    WalletTransactionRepository as TransactionRepository,
)
from app.wallet.presentation.dtos.response import (
    WalletResponse,
    WalletTransactionResponse as TransactionResponse,
)
from ...query.queries import GetWalletByIdQuery, GetWalletByUserIdQuery


class GetWalletByIdUseCase:
    """Use case for retrieving a wallet by its ID."""

    def __init__(
        self, wallet_repo: WalletRepository, transaction_repo: TransactionRepository
    ):
        self.wallet_repo = wallet_repo
        self.transaction_repo = transaction_repo

    async def execute(self, query: GetWalletByIdQuery) -> WalletResponse:
        """Retrieves a wallet by its ID."""
        wallet = await self.wallet_repo.get_by_id(query.walletId, raise_exception=True)

        response = WalletResponse.from_domain(wallet)

        if query.include_transactions:
            await self._get_transactions(query, response)

        return response

    async def _get_transactions(self, query, dto):
        transactions = await self.transaction_repo.list_by_wallet_id(query)
        dto.transactions = [TransactionResponse.from_domain(t) for t in transactions]


class GetWalletsByUserIdUseCase:
    """Use case for retrieving all wallets for a given user."""

    def __init__(
        self, wallet_repo: WalletRepository, transaction_repo: TransactionRepository
    ):
        self.wallet_repo = wallet_repo
        self.transaction_repo = transaction_repo

    async def execute(self, query: GetWalletByUserIdQuery) -> WalletResponse:
        """Retrieves all wallets for a given user."""
        wallet = await self.wallet_repo.get_by_user_id(
            user_id=query.userId,
            raise_exception=True,
        )

        return WalletResponse.from_domain(wallet)

    async def _get_transactions(self, query, dto):
        transactions = await self.transaction_repo.list_by_wallet_id(query)
        dto.transactions = [TransactionResponse.from_domain(t) for t in transactions]
