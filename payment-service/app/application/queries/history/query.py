from pydantic import BaseModel, Field, UUID4, validator
from typing import Optional
from datetime import datetime
from app.shared.sort import PaymentSortBy, SortOrder

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
