import uuid
from decimal import Decimal
from ..value_objects import Money, WalletId
from typing import Optional
from datetime import datetime
from app.wallet.domain.enums import TransactionType
from app.wallet.domain.value_objects import PaymentDetails


class WalletTransaction:
    def __init__(
        self,
        transaction_id: uuid.UUID,
        wallet_id: WalletId,
        amount: Money,
        transaction_type: TransactionType,
        payment_details: PaymentDetails,
        timestamp: Optional[datetime] = None,
    ):
        self.transaction_id = transaction_id
        self.wallet_id = wallet_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.payment_details = payment_details
        self.timestamp = timestamp if timestamp else datetime.now()

    def __repr__(self):
        return (
            f"WalletTransaction(id={self.transaction_id}, wallet_id={self.wallet_id.value}, "
            f"amount={self.amount}, type={self.transaction_type.value}, "
            f"timestamp={self.timestamp})"
        )

    @classmethod
    def create(cls, wallet_id, amount, transaction_type, payment_details):
        return cls(
            transaction_id=uuid.uuid4(),
            wallet_id=wallet_id,
            amount=amount,
            payment_details=payment_details,
            transaction_type=transaction_type,
            timestamp=datetime.now(),
        )
