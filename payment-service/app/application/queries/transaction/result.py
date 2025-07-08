from pydantic import BaseModel
from typing import Optional, List
from ...dto.response import TransactionDetail, PaymentDetail, WalletDetail

class GetTransactionResult(BaseModel):
    """Result of transaction query."""
    transaction: Optional['TransactionDetail'] = None
    payment: Optional['PaymentDetail'] = None
    wallet: Optional['WalletDetail'] = None
    related_transactions: List['TransactionDetail'] = []
    found: bool = False
    message: str = ""


