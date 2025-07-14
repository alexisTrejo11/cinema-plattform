from typing import List, Optional
from .wallet_query_usecases import (
    WalletRepository,
    GetWalletByIdUseCase,
    GetWalletsByUserIdUseCase,
    WalletResponse,
)
from .wallet_command_use_cases import (
    InitWalletForUserUseCase,
    PayWithWalletUseCase,
    AddCreditUseCase,
    CreateWalletCommand,
    BuyCreditResponse,
    PayWithWalletCommand,
    WalletBuyResponse,
    AddCreditCommand,
)
from app.wallet.domain.repositories.transaction_repository import (
    WalletTransactionRepository,
)
from uuid import UUID


class WalletUseCases:
    """Container for all wallet use cases - useful for dependency injection."""

    def __init__(
        self,
        wallet_repo: WalletRepository,
        transaction_repository: WalletTransactionRepository,
    ):
        self._add_credit = AddCreditUseCase(wallet_repo, transaction_repository)
        self._pay = PayWithWalletUseCase(wallet_repo, transaction_repository)
        self._create_wallet = InitWalletForUserUseCase(wallet_repo)
        self._get_wallet_by_id = GetWalletByIdUseCase(wallet_repo)
        self._get_wallets_by_user_id = GetWalletsByUserIdUseCase(wallet_repo)

    async def create_wallet(self, command: CreateWalletCommand) -> BuyCreditResponse:
        return await self._create_wallet.execute(command)

    async def get_wallet_by_id(self, wallet_id: UUID) -> Optional[WalletResponse]:
        return await self._get_wallet_by_id.execute(wallet_id)

    async def get_wallets_by_user_id(self, user_id: UUID) -> List[WalletResponse]:
        return await self._get_wallets_by_user_id.execute(user_id)

    async def add_credit(self, command: AddCreditCommand) -> BuyCreditResponse:
        return await self._add_credit.execute(command)

    async def pay(self, command: PayWithWalletCommand) -> WalletBuyResponse:
        return await self._pay.execute(command)
