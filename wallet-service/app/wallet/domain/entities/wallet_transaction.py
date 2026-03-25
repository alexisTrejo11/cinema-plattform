from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field

from ..enums import TransactionType
from ..value_objects import (
    Money,
    PaymentDetails,
    WalletId,
    WalletTransactionId,
)


class WalletTransaction(BaseModel):
    """
    Immutable record of a single wallet operation.
    Pydantic provides __repr__, __eq__, and model_dump() — to_dict() removed.
    timestamp defaults to UTC-naive datetime (stripped tzinfo) for DB consistency.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    transaction_id: WalletTransactionId
    wallet_id: WalletId
    amount: Money
    transaction_type: TransactionType
    payment_details: PaymentDetails
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )

    @classmethod
    def create(
        cls,
        wallet_id: WalletId,
        amount: Money,
        transaction_type: TransactionType,
        payment_details: PaymentDetails,
    ) -> "WalletTransaction":
        return cls(
            transaction_id=WalletTransactionId.generate(),
            wallet_id=wallet_id,
            amount=amount,
            transaction_type=transaction_type,
            payment_details=payment_details,
        )
