from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.wallet.domain.value_objects import WalletId, UserId


class QueryBase(BaseModel):
    # pydantic_settings.SettingsConfigDict was incorrectly used here before;
    # pydantic.ConfigDict is the correct choice for plain BaseModel subclasses.
    model_config = ConfigDict(arbitrary_types_allowed=True)

    offset: int = 0
    limit: int = 10
    sort_by: str = "created_at"
    sort_direction: str = "asc"


class TransactionByWalletQuery(QueryBase):
    walletId: WalletId


class GetWalletByIdQuery(TransactionByWalletQuery):
    include_transactions: bool = False


class GetWalletByUserIdQuery(QueryBase):
    userId: UserId
    include_transactions: bool = False


class WalletSummaryQuery(BaseModel):
    """Resolve a wallet by user or wallet id, then aggregate transactions (optional date window)."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    userId: Optional[UserId] = None
    walletId: Optional[WalletId] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None


class SearchTransactionQuery(QueryBase):
    userId: Optional[UserId] = Field(
        None, description="Filter by user ID associated with the transaction."
    )
    walletId: Optional[WalletId] = Field(
        None, description="Filter by wallet ID associated with the transaction."
    )
    type: Optional[str] = Field(
        None, description="Filter by transaction type (e.g., 'deposit', 'withdrawal')."
    )
    min_amount: Optional[str] = Field(
        None, description="Minimum transaction amount (inclusive)."
    )
    max_amount: Optional[str] = Field(
        None, description="Maximum transaction amount (inclusive)."
    )
    created_before: Optional[datetime] = Field(
        None, description="Transactions created before this datetime."
    )
    created_after: Optional[datetime] = Field(
        None, description="Transactions created after this datetime."
    )
    payment_method: Optional[str] = Field(
        None,
        description="Filter by payment method (e.g., 'credit_card', 'bank_transfer').",
    )
    payment_id: Optional[UUID] = Field(
        None, description="Filter by specific payment gateway ID."
    )


class SearchWalletQuery(QueryBase):
    userId: UserId
    walletId: WalletId
    balance: str
