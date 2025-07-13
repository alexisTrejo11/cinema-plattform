import uuid
from decimal import Decimal
from ..value_objects import Money, WalletId
from typing import Optional
from datetime import datetime
from app.wallet.domain.enums import TransactionType


class PaymentDetails:
    def __init__(self, payment_method: str, payment_id: uuid.UUID):
        self.payment_method = payment_method
        self.payment_id = payment_id

    def __repr__(self):
        return (
            f"PaymentDeal(payment_id={self.payment_id}, method={self.payment_method})"
        )


class WalletTransaction:
    def __init__(
        self,
        transaction_id: uuid.UUID,
        wallet_id: WalletId,
        amount: Money,
        transaction_type: TransactionType,
        payment_details: Optional[PaymentDetails] = None,
        timestamp: Optional[datetime] = None,
    ):
        self.transaction_id = transaction_id
        self.wallet_id = wallet_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.payment_details = payment_details
        self.timestamp = timestamp if timestamp else datetime.utcnow()

    def __repr__(self):
        return (
            f"WalletTransaction(id={self.transaction_id}, wallet_id={self.wallet_id.value}, "
            f"amount={self.amount}, type={self.transaction_type.value}, "
            f"timestamp={self.timestamp})"
        )
