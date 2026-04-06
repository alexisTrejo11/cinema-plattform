"""Application-layer result types."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.wallet.domain.entities import Wallet, WalletTransaction
from app.wallet.domain.summary import TransactionTypeAggregateRow


class WalletSummaryResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    wallet_id: UUID
    user_id: UUID
    balance_display: str
    currency: str
    total_transactions: int
    by_transaction_type: list[TransactionTypeAggregateRow]


@dataclass(frozen=True)
class WalletOperationOutcome:
    """Wallet + persisted transaction after add-credit or pay flows."""

    wallet: Wallet
    transaction: WalletTransaction
