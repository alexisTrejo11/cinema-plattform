from decimal import Decimal
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
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


class SearchTicketParams(BaseModel):
    movie_id: Optional[int] = Field(
        default=None,
        description="Filter by movie ID",
        json_schema_extra={"example": 123}
    )
    showtime_id: Optional[int] = Field(
        default=None,
        description="Filter by showtime ID",
        json_schema_extra={"example": 456}
    )
    user_id: Optional[int] = Field(
        default=None,
        description="Filter by user ID",
        json_schema_extra={"example": 789}
    )
    status: Optional[TicketStatus] = Field(
        default=None,
        description="Filter by ticket status",
        json_schema_extra={"example": "purchased"}
    )
    include_seats: bool = Field(
        default=False,
        description="Include seat information in response"
    )
    created_before: Optional[datetime] = Field(
        default=None,
        description="Filter tickets created before this datetime",
        json_schema_extra={"example": "2023-01-01T00:00:00"}
    )
    created_after: Optional[datetime] = Field(
        default=None,
        description="Filter tickets created after this datetime",
        json_schema_extra={"example": "2023-01-01T00:00:00"}
    )
    updated_before: Optional[datetime] = Field(
        default=None,
        description="Filter tickets updated before this datetime"
    )
    updated_after: Optional[datetime] = Field(
        default=None,
        description="Filter tickets updated after this datetime"
    )
    price_min: Optional[float] = Field(
        default=None,
        ge=0,
        description="Minimum ticket price",
        json_schema_extra={"example": 10.50}
    )
    price_max: Optional[float] = Field(
        default=None,
        ge=0,
        description="Maximum ticket price",
        json_schema_extra={"example": 25.00}
    )
    page_limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of items per page (1-100)"
    )
    page_offset: int = Field(
        default=0,
        ge=0,
        description="Pagination offset"
    )
    sort_by: str = Field(
        default="created_at",
        description="Field to sort by (created_at, updated_at, price)",
        json_schema_extra={"example": "price"}
    )
    sort_direction_asc: bool = Field(
        default=True,
        description="Sort direction (True for ascending, False for descending)"
    )

    @field_validator('price_max')
    @classmethod
    def validate_price_range(cls, v: Optional[float], info):
        if 'price_min' in info.data and v is not None and info.data['price_min'] is not None:
            if v < info.data['price_min']:
                raise ValueError('price_max must be greater than or equal to price_min')
        return v

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "movie_id": 123,
                "showtime_id": 456,
                "user_id": 789,
                "status": "purchased",
                "include_seats": True,
                "created_after": "2023-01-01T00:00:00",
                "price_min": 10.00,
                "price_max": 25.00,
                "page_limit": 20,
                "sort_by": "price",
                "sort_direction_asc": False
            }
        }


class SeatInfo(BaseModel):
    id: int = Field(..., json_schema_extra={"example": 1})
    seat_number: str = Field(..., json_schema_extra={"example": "A12"})
    row: str = Field(..., json_schema_extra={"example": "A"})
    number: int = Field(..., json_schema_extra={"example": 12})
    type: str = Field(..., json_schema_extra={"example": "VIP"})

class TicketResponse(BaseModel):
    id: int = Field(..., json_schema_extra={"example": 123})
    user_id: int = Field(..., json_schema_extra={"example": 456})
    movie_id: int = Field(..., json_schema_extra={"example": 789})
    showtime_id: int = Field(..., json_schema_extra={"example": 101})
    price: float = Field(..., json_schema_extra={"example": 12.50})
    price_currency: str = Field(..., json_schema_extra={"example": "USD"})
    status: TicketStatus = Field(..., json_schema_extra={"example": "purchased"})
    created_at: datetime = Field(..., json_schema_extra={"example": "2023-01-01T12:00:00Z"})
    seats: List[SeatInfo] = Field(
        default_factory=list, 
        description="List of associated seats",
        json_schema_extra={"example": [{
            "id": 1,
            "seat_number": "A12",
            "row": "A",
            "number": 12,
            "type": "VIP"
        }]}
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 123,
                "user_id": 456,
                "movie_id": 789,
                "showtime_id": 101,
                "price": 12.50,
                "price_currency": "USD",
                "status": "purchased",
                "created_at": "2023-01-01T12:00:00Z",
                "seats": [{
                    "id": 1,
                    "seat_number": "A12",
                    "row": "A",
                    "number": 12,
                    "type": "VIP"
                }]
            }
        }
    )
        
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
    
