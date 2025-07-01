from decimal import Decimal
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from app.ticket.domain.valueobjects.enums import TicketStatus


class CreateTicketData(BaseModel):
    user_id: int = Field(..., gt=0, description="User ID")
    movie_id: int = Field(..., gt=0, description="Movie ID")
    showtime_id: int = Field(..., gt=0, description="Showtime ID")
    seat_number: str = Field(..., min_length=1, max_length=10, description="Seat number")
    seat_type: str = Field(..., description="Seat type")
    price: float = Field(..., gt=0, description="Ticket price")

class UpdateTicketData(BaseModel):
    seat_number: Optional[str] = Field(None, min_length=1, max_length=10)
    seat_type: Optional[str] = None


class TicketResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    showtime_id: int
    seat_number: str
    seat_type: str
    price: float
    status: TicketStatus
    reservation_time: datetime
    confirmation_time: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True
        

class TicketListResponst(BaseModel):
    tickets: List['TicketResponse']
    total: int
    page: int
    per_page: int


class ConfirmTicket(BaseModel):
    ticket_id: int = Field(..., gt=0)


class RefundRequest(BaseModel):
    ticket_id: int = Field(..., gt=0)
    reason: Optional[str] = Field(None, max_length=500)


class RefundResponse(BaseModel):
    ticket_id: int
    refund_amount: Decimal
    processing_fee: Decimal
    net_refund: Decimal
    status: str
    
    