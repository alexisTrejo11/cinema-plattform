from decimal import Decimal
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List, Optional
from app.ticket.domain.valueobjects.enums import TicketStatus, TicketType

class CreateTicketData(BaseModel):
    user_id: int = Field(..., gt=0, description="User ID")
    movie_id: int = Field(..., gt=0, description="Movie ID")
    showtime_id: int = Field(..., gt=0, description="Showtime ID")
    seat_number: str = Field(..., min_length=1, max_length=10, description="Seat number")
    seat_type: str = Field(..., description="Seat type")
    price: float = Field(..., gt=0, description="Ticket price")


class BuyTicketsRequest(BaseModel):
    user_email: EmailStr = Field(..., gt=0, description="Customer Email")
    customer_id: int = Field(..., gt=0, description="Customer ID")
    showtime_id: int = Field(..., gt=0, description="Showtime ID")
    seat_list_id: List[int] = Field([])
    payment_method:  str
    ticket_type:  TicketType = Field(...)
    payment_deatils: str
    customer_ip: str
    
    


class TicketDetailResponse(BaseModel):
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
        
        
class TicketBuyedResponse(BaseModel):
    """ DTO retrived to customer after ticket buying"""
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
    tickets: List['TicketDetailResponse']
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
    
