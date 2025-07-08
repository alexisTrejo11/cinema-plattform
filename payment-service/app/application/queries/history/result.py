from pydantic import BaseModel
from typing import List
from ...dto.response import PaymentHistoryItem

class PaymentHistoryResult(BaseModel):
    """Result of payment history query."""
    payments: List[PaymentHistoryItem]
    total_count: int
    has_more: bool
    limit: int
    offset: int


    @staticmethod
    def return_failure(limit: int = 0, offset = 0) -> 'PaymentHistoryResult':
        """
        Return a failure result with empty payments and default values.
        
        Returns:
            PaymentHistoryResult: An instance with empty payments and default values.
        """
        return PaymentHistoryResult(
            payments=[],
            total_count=0,
            has_more=False,
            limit=limit,
            offset=offset
        )