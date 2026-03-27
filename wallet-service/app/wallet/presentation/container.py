from __future__ import annotations

from app.wallet.application.use_cases.wallet_command_use_cases import (
    AddCreditUseCase,
    InitWalletForUserUseCase,
    PayWithWalletUseCase,
)
from app.wallet.application.use_cases.wallet_query_use_cases import (
    GetWalletByIdUseCase,
    GetWalletsByUserIdUseCase,
    ListWalletTransactionsUseCase,
)
from app.wallet.application.use_cases.wallet_summary_use_cases import (
    GetWalletSummaryUseCase,
)
from app.wallet.domain.interfaces import (
    UserInternalService,
    WalletEventPublisher,
    WalletRepository,
    WalletTransactionRepository,
)


class WalletUseCases:
    """Facade wiring wallet use cases for FastAPI dependency injection."""

    def __init__(
        self,
        wallet_repo: WalletRepository,
        transaction_repository: WalletTransactionRepository,
        user_service: UserInternalService,
        event_publisher: WalletEventPublisher,
    ) -> None:
        self._add_credit = AddCreditUseCase(
            wallet_repo, transaction_repository, event_publisher
        )
        self._pay = PayWithWalletUseCase(
            wallet_repo, transaction_repository, event_publisher
        )
        self._create_wallet = InitWalletForUserUseCase(wallet_repo, user_service)
        self._get_wallet_by_id = GetWalletByIdUseCase(
            wallet_repo, transaction_repository
        )
        self._get_wallets_by_user_id = GetWalletsByUserIdUseCase(
            wallet_repo, transaction_repository
        )
        self._list_wallet_transactions = ListWalletTransactionsUseCase(
            transaction_repository
        )
        self._get_wallet_summary = GetWalletSummaryUseCase(
            wallet_repo, transaction_repository
        )

    async def create_wallet(self, command):
        return await self._create_wallet.execute(command)

    async def get_wallet_by_id(self, query):
        return await self._get_wallet_by_id.execute(query)

    async def get_wallets_by_user_id(self, query):
        return await self._get_wallets_by_user_id.execute(query)

    async def list_wallet_transactions(self, query):
        return await self._list_wallet_transactions.execute(query)

    async def get_wallet_summary(self, query):
        return await self._get_wallet_summary.execute(query)

    async def add_credit(self, command):
        return await self._add_credit.execute(command)

    async def pay(self, command):
        return await self._pay.execute(command)
