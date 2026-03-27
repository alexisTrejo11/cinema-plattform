from __future__ import annotations

from app.wallet.application.queries import (
    GetWalletByIdQuery,
    GetWalletByUserIdQuery,
    TransactionByWalletQuery,
)
from app.wallet.domain.interfaces import WalletRepository, WalletTransactionRepository
from app.wallet.presentation.dtos.response import WalletResponse


class GetWalletByIdUseCase:
    def __init__(
        self,
        wallet_repo: WalletRepository,
        transaction_repo: WalletTransactionRepository,
    ) -> None:
        self._wallet_repo = wallet_repo
        self._transaction_repo = transaction_repo

    async def execute(self, query: GetWalletByIdQuery) -> WalletResponse:
        wallet = await self._wallet_repo.get_by_id(
            query.walletId,
            raise_exception=True,
        )
        if query.include_transactions:
            tq = TransactionByWalletQuery(
                walletId=query.walletId,
                offset=query.offset,
                limit=query.limit,
                sort_by=query.sort_by,
                sort_direction=query.sort_direction,
            )
            txs = await self._transaction_repo.list_by_wallet_id(tq)
            wallet.set_transactions(txs)
        return WalletResponse.from_domain(wallet)


class GetWalletsByUserIdUseCase:
    def __init__(
        self,
        wallet_repo: WalletRepository,
        transaction_repo: WalletTransactionRepository,
    ) -> None:
        self._wallet_repo = wallet_repo
        self._transaction_repo = transaction_repo

    async def execute(self, query: GetWalletByUserIdQuery) -> WalletResponse:
        wallet = await self._wallet_repo.get_by_user_id(
            query.userId,
            raise_exception=True,
        )
        if query.include_transactions:
            tq = TransactionByWalletQuery(
                walletId=wallet.id,
                offset=query.offset,
                limit=query.limit,
                sort_by=query.sort_by,
                sort_direction=query.sort_direction,
            )
            txs = await self._transaction_repo.list_by_wallet_id(tq)
            wallet.set_transactions(txs)
        return WalletResponse.from_domain(wallet)
