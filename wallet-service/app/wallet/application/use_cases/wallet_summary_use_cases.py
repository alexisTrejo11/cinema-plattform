from __future__ import annotations

import logging

from app.shared.base_exceptions import NotFoundException, ValidationException
from app.wallet.application.queries import WalletSummaryQuery
from app.wallet.application.results import WalletSummaryResult
from app.wallet.domain.entities import Wallet
from app.wallet.domain.interfaces import (
    WalletRepository,
    WalletTransactionRepository,
)

logger = logging.getLogger(__name__)


class GetWalletSummaryUseCase:
    """
    Builds balance + transaction aggregates for a wallet.
    Callers enforce authorization (customer vs staff); this use case only resolves data.
    """

    def __init__(
        self,
        wallet_repo: WalletRepository,
        transaction_repo: WalletTransactionRepository,
    ) -> None:
        self._wallet_repo = wallet_repo
        self._transaction_repo = transaction_repo

    async def execute(self, query: WalletSummaryQuery) -> WalletSummaryResult:
        if query.userId and query.walletId:
            raise ValidationException(
                "walletId",
                "Provide only one of userId or walletId.",
            )
        if not query.userId and not query.walletId:
            raise ValidationException(
                "userId",
                "Provide userId or walletId.",
            )

        wallet: Wallet | None
        if query.walletId:
            wallet = await self._wallet_repo.find_by_id(query.walletId)
            if not wallet:
                raise NotFoundException("Wallet", query.walletId.value, "wallet_id")
        else:
            wallet = await self._wallet_repo.find_by_user_id(query.userId)  # type: ignore[arg-type]
            if not wallet:
                raise NotFoundException("Wallet", query.userId.value, "user_id")  # type: ignore[union-attr]

        total, rows = await self._transaction_repo.aggregate_by_wallet_id(
            wallet.id,
            created_after=query.created_after,
            created_before=query.created_before,
        )

        logger.info(
            "Wallet summary wallet_id=%s total_tx=%s window=%s..%s",
            wallet.id.value,
            total,
            query.created_after,
            query.created_before,
        )

        return WalletSummaryResult(
            wallet_id=wallet.id.value,
            user_id=wallet.user_id.value,
            balance_display=str(wallet.balance.amount),
            currency=wallet.balance.currency.value,
            total_transactions=total,
            by_transaction_type=rows,
        )
