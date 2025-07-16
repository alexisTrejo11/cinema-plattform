from typing import List, Optional
from uuid import UUID
from .wallet.wallet_query_usecases import (
    WalletRepository,
    GetWalletByIdUseCase,
    GetWalletsByUserIdUseCase,
)
from .wallet.wallet_command_use_cases import (
    InitWalletForUserUseCase,
    PayWithWalletUseCase,
    AddCreditUseCase,
)
from ..query.queries import GetWalletByIdQuery, GetWalletByUserIdQuery
from app.wallet.domain.repositories.transaction_repository import (
    WalletTransactionRepository,
)
from app.user.domain.repository import UserRepository
from app.wallet.application.command.commands import (
    PayWithWalletCommand,
    CreateWalletCommand,
    AddCreditCommand,
)
from app.wallet.presentation.dtos.response import WalletResponse, WalletBuyResponse
from app.wallet.application.event_publisher import WalletEventPublisher


class WalletUseCases:
    """Container for all wallet use cases - useful for dependency injection."""

    def __init__(
        self,
        wallet_repo: WalletRepository,
        transaction_repository: WalletTransactionRepository,
        user_repository: UserRepository,
        event_publisher: WalletEventPublisher,
    ):
        self._add_credit = AddCreditUseCase(
            wallet_repo, transaction_repository, event_publisher
        )
        self._pay = PayWithWalletUseCase(
            wallet_repo, transaction_repository, event_publisher
        )
        self._create_wallet = InitWalletForUserUseCase(wallet_repo, user_repository)
        self._get_wallet_by_id = GetWalletByIdUseCase(wallet_repo)
        self._get_wallets_by_user_id = GetWalletsByUserIdUseCase(wallet_repo)

    async def create_wallet(self, command: CreateWalletCommand) -> WalletResponse:
        return await self._create_wallet.execute(command)

    async def get_wallet_by_id(self, query: GetWalletByIdQuery) -> WalletResponse:
        return await self._get_wallet_by_id.execute(query)

    async def get_wallets_by_user_id(
        self, query: GetWalletByUserIdQuery
    ) -> WalletResponse:
        return await self._get_wallets_by_user_id.execute(query)

    async def add_credit(self, command: AddCreditCommand) -> WalletBuyResponse:
        return await self._add_credit.execute(command)

    async def pay(self, command: PayWithWalletCommand) -> WalletBuyResponse:
        return await self._pay.execute(command)
