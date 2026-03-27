from __future__ import annotations

from app.wallet.domain.entities import Wallet, WalletTransaction
from app.wallet.domain.interfaces import (
    TransactionEvents,
    WalletEventPublisher,
)


class NoOpWalletEventPublisher(WalletEventPublisher):
    async def publish_event(
        self,
        user_wallet: Wallet,
        new_transaction: WalletTransaction,
        event_type: TransactionEvents,
    ) -> None:
        return None
