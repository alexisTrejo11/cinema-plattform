"""FastAPI query / dependency models shared by wallet controllers."""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, ConfigDict

from app.shared.core.pagination import PaginationParams
from app.wallet.application.queries import (
    GetWalletByIdQuery,
    GetWalletByUserIdQuery,
    TransactionByWalletQuery,
    WalletSummaryQuery,
)
from app.wallet.domain.value_objects import UserId, WalletId


class WalletPagedQueryParams(PaginationParams):
    """Pagination plus whether to embed transactions (staff / customer wallet reads)."""

    include_transactions: bool = Query(
        default=False,
        description="If true, includes transactions for the wallet (subject to page/limit).",
    )

    def to_get_wallet_by_id_query(self, wallet_id: UUID) -> GetWalletByIdQuery:
        return GetWalletByIdQuery(
            walletId=WalletId(value=wallet_id),
            include_transactions=self.include_transactions,
            limit=self.limit,
            offset=self.offset,
        )

    def to_get_wallet_by_user_id_query(self, user_id: UUID) -> GetWalletByUserIdQuery:
        return GetWalletByUserIdQuery(
            userId=UserId(value=user_id),
            include_transactions=self.include_transactions,
            limit=self.limit,
            offset=self.offset,
        )


class WalletTransactionListQueryParams(PaginationParams):
    """Pagination and sort for listing a wallet’s transactions."""

    sort_by: str = Query(
        default="timestamp",
        description="Column on wallet_transactions to sort by (e.g. timestamp, created_at).",
    )
    sort_direction: Literal["asc", "desc"] = Query(
        default="desc",
        description="Sort direction.",
    )

    def to_transaction_by_wallet_query(self, wallet_id: WalletId) -> TransactionByWalletQuery:
        return TransactionByWalletQuery(
            walletId=wallet_id,
            offset=self.offset,
            limit=self.limit,
            sort_by=self.sort_by,
            sort_direction=self.sort_direction,
        )


class WalletManagementSummaryQueryParams(BaseModel):
    """Staff wallet summary: target by user or wallet id, optional time window."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    user_id: UUID | None = None
    wallet_id: UUID | None = None
    created_after: datetime | None = None
    created_before: datetime | None = None

    def to_wallet_summary_query(self) -> WalletSummaryQuery:
        return WalletSummaryQuery(
            userId=UserId(value=self.user_id) if self.user_id else None,
            walletId=WalletId(value=self.wallet_id) if self.wallet_id else None,
            created_after=self.created_after,
            created_before=self.created_before,
        )


def get_wallet_management_summary_params(
    user_id: UUID | None = Query(
        None,
        description="Target user id; provide exactly one of user_id or wallet_id.",
    ),
    wallet_id: UUID | None = Query(
        None,
        description="Target wallet id; provide exactly one of user_id or wallet_id.",
    ),
    created_after: datetime | None = Query(
        None,
        description="Include transactions with timestamp >= this (optional).",
    ),
    created_before: datetime | None = Query(
        None,
        description="Include transactions with timestamp <= this (optional).",
    ),
) -> WalletManagementSummaryQueryParams:
    return WalletManagementSummaryQueryParams(
        user_id=user_id,
        wallet_id=wallet_id,
        created_after=created_after,
        created_before=created_before,
    )
