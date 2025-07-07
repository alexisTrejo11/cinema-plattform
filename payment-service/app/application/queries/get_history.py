from pydantic import BaseModel, Field, UUID4, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum

from app.domain.value_objects import (
    UserId, PaymentId, PaymentStatus, PaymentType
)
from app.domain.repository.payment_repository import PaymentRepository
from app.application.interfaces import TransactionRepository


class PaymentSortBy(str, Enum):
    """Payment history sorting options."""
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    AMOUNT = "amount"
    STATUS = "status"


class SortOrder(str, Enum):
    """Sort order options."""
    ASC = "asc"
    DESC = "desc"


class GetPaymentHistoryQuery(BaseModel):
    """Query to get payment history for a user."""
    user_id: UUID4 = Field(..., description="ID of the user to get payment history for.")
    status: Optional[str] = Field(None, description="Filter by payment status.")
    payment_type: Optional[str] = Field(None, description="Filter by payment type.")
    start_date: Optional[datetime] = Field(None, description="Start date for filtering.")
    end_date: Optional[datetime] = Field(None, description="End date for filtering.")
    limit: int = Field(50, ge=1, le=100, description="Maximum number of records to return.")
    offset: int = Field(0, ge=0, description="Number of records to skip.")
    sort_by: PaymentSortBy = Field(PaymentSortBy.CREATED_AT, description="Field to sort by.")
    sort_order: SortOrder = Field(SortOrder.DESC, description="Sort order.")

    @validator('end_date')
    def end_date_after_start_date(cls, v, values):
        if v and 'start_date' in values and values['start_date']:
            if v < values['start_date']:
                raise ValueError('end_date must be after start_date')
        return v

    class Config:
        schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "status": "completed",
                "payment_type": "ticket_purchase",
                "start_date": "2024-01-01T00:00:00Z",
                "end_date": "2024-12-31T23:59:59Z",
                "limit": 25,
                "offset": 0,
                "sort_by": "created_at",
                "sort_order": "desc"
            }
        }


class PaymentHistoryItem(BaseModel):
    """Individual payment history item."""
    payment_id: UUID
    user_id: UUID
    amount: float
    currency: str
    payment_method: str
    payment_type: str
    status: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    failure_reason: Optional[str] = None
    refunded_amount: float = 0.0
    refund_reason: Optional[str] = None
    refunded_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class PaymentHistoryResult(BaseModel):
    """Result of payment history query."""
    payments: List[PaymentHistoryItem]
    total_count: int
    has_more: bool
    limit: int
    offset: int


class GetPaymentHistoryQueryHandler:
    """Handler for getting payment history."""
    
    def __init__(self, payment_repository: PaymentRepository):
        self.payment_repository = payment_repository
    
    async def handle(self, query: GetPaymentHistoryQuery) -> PaymentHistoryResult:
        """
        Handle payment history query.
        
        Args:
            query: Payment history query
            
        Returns:
            Payment history result
        """
        try:
            # Build filter criteria
            filters = {
                'user_id': UserId.from_string(str(query.user_id))
            }
            
            if query.status:
                filters['status'] = PaymentStatus(query.status)
            
            if query.payment_type:
                filters['payment_type'] = PaymentType(query.payment_type)
            
            if query.start_date:
                filters['created_after'] = query.start_date
            
            if query.end_date:
                filters['created_before'] = query.end_date
            
            # Add pagination and sorting
            filters.update({
                'limit': query.limit + 1,  # Request one extra to check if there are more
                'offset': query.offset,
                'sort_by': query.sort_by.value,
                'sort_order': query.sort_order.value
            })
            
            # Get payments from repository
            payments = await self.payment_repository.list(**filters)
            
            # Check if there are more records
            has_more = len(payments) > query.limit
            if has_more:
                payments = payments[:query.limit]  # Remove the extra record
            
            # Convert to response format
            payment_items = [
                PaymentHistoryItem(
                    payment_id=payment.id.value,
                    user_id=payment.user_id.value,
                    amount=payment.amount.to_float(),
                    currency=payment.amount.currency.value,
                    payment_method=payment.payment_method.value,
                    payment_type=payment.payment_type.value,
                    status=payment.status.value,
                    created_at=payment.created_at,
                    updated_at=payment.updated_at,
                    completed_at=payment.completed_at,
                    failure_reason=payment.failure_reason,
                    refunded_amount=payment.refunded_amount.to_float() if payment.refunded_amount else 0.0,
                    refund_reason=payment.refund_reason,
                    refunded_at=payment.refunded_at,
                    metadata=payment.metadata.__dict__ if payment.metadata else None
                )
                for payment in payments
            ]
            
            return PaymentHistoryResult(
                payments=payment_items,
                total_count=len(payment_items),  # This would ideally come from a separate count query
                has_more=has_more,
                limit=query.limit,
                offset=query.offset
            )
            
        except Exception as e:
            # Return empty result on error
            return PaymentHistoryResult(
                payments=[],
                total_count=0,
                has_more=False,
                limit=query.limit,
                offset=query.offset
            )
