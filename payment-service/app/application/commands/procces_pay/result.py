from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ProcessPaymentResult(BaseModel):
    """Result of payment processing."""
    payment_id: UUID
    status: str
    message: str
    transaction_reference: Optional[str] = None
