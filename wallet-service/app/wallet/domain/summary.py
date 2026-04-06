from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.wallet.domain.enums import TransactionType


class TransactionTypeAggregateRow(BaseModel):
    """Per–transaction-type counts and volume for a wallet."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    transaction_type: TransactionType
    count: int
    total_amount: Decimal
