import logging
from typing import List

from app.wallet.domain.interfaces import WalletRepository, WalletTransactionRepository
from app.wallet.domain.exceptions import WalletNotFoundError
from app.wallet.domain.entities import Wallet, WalletTransaction

from ..queries import (
    GetWalletByIdQuery,
    GetWalletByUserIdQuery,
    TransactionByWalletQuery,
)

logger = logging.getLogger(__name__)


class GetWalletByIdUseCase:
    def __init__(
        self,
        wallet_repository: WalletRepository,
        transaction_repository: WalletTransactionRepository,
    ) -> None:
        self._wallet_repository = wallet_repository
        self._transaction_repository = transaction_repository

    async def execute(self, query: GetWalletByIdQuery) -> Wallet:
        wallet = await self._wallet_repository.find_by_id(query.walletId)
        if not wallet:
            raise WalletNotFoundError(query.walletId)

        logger.info(
            "Loaded wallet by id=%s include_transactions=%s",
            query.walletId.value,
            query.include_transactions,
        )

        if query.include_transactions:
            tq = TransactionByWalletQuery(
                walletId=query.walletId,
                offset=query.offset,
                limit=query.limit,
                sort_by=query.sort_by,
                sort_direction=query.sort_direction,
            )
            txs = await self._transaction_repository.find_by_wallet_id(tq)
            wallet.set_transactions(txs)

        return wallet


class GetWalletTransactionsUseCase:
    def __init__(self, transaction_repository: WalletTransactionRepository) -> None:
        self._transaction_repository = transaction_repository

    async def execute(self, query: TransactionByWalletQuery) -> List[WalletTransaction]:
        logger.info(
            "Listing transactions for wallet_id=%s offset=%s limit=%s",
            query.walletId.value,
            query.offset,
            query.limit,
        )
        return await self._transaction_repository.find_by_wallet_id(query)


class GetWalletsByUserIdUseCase:
    def __init__(
        self,
        wallet_repository: WalletRepository,
        transaction_repository: WalletTransactionRepository,
    ) -> None:
        self._wallet_repository = wallet_repository
        self._transaction_repository = transaction_repository

    async def execute(self, query: GetWalletByUserIdQuery) -> Wallet:
        wallet = await self._wallet_repository.find_by_user_id(query.userId)
        if not wallet:
            raise WalletNotFoundError(query.userId)

        logger.info(
            "Loaded wallet by user_id=%s include_transactions=%s",
            query.userId.value,
            query.include_transactions,
        )

        if query.include_transactions:
            tq = TransactionByWalletQuery(
                walletId=wallet.id,
                offset=query.offset,
                limit=query.limit,
                sort_by=query.sort_by,
                sort_direction=query.sort_direction,
            )
            txs = await self._transaction_repository.find_by_wallet_id(tq)
            wallet.set_transactions(txs)

        return wallet
