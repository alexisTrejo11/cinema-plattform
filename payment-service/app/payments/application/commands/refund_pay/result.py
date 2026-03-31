from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class RefundPaymentResult(BaseModel):
    """Result of payment refund."""
    payment_id: UUID
    refund_amount: float
    status: str
    message: str
    transaction_reference: Optional[str] = None
    refunded_to_wallet: bool = False
