from decimal import Decimal
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from datetime import datetime
from typing import List, Optional
from app.ticket.domain.valueobjects.enums import TicketStatus, TicketType


class BuyTicketsRequest(BaseModel):
    """Request DTO for purchasing tickets online.

    Contains all necessary information to process a ticket purchase transaction.
    """

    user_email: EmailStr = Field(
        ...,
        description="Customer's verified email address for ticket delivery",
        json_schema_extra={"example": "customer@example.com"},
    )
    customer_id: int = Field(
        ...,
        gt=0,
        description="Unique identifier of the customer making the purchase",
        json_schema_extra={"example": 12345},
    )
    showtime_id: int = Field(
        ...,
        gt=0,
        description="ID of the showtime being booked",
        json_schema_extra={"example": 789},
    )
    seat_list_id: List[int] = Field(
        [],
        description="List of seat IDs being reserved",
        json_schema_extra={"example": [101, 102, 103]},
    )
    payment_method: str = Field(
        ...,
        description="Payment method identifier (e.g., 'credit_card', 'paypal')",
        json_schema_extra={"example": "credit_card"},
    )
    ticket_type: TicketType = Field(
        ...,
        description="Type of ticket being purchased",
        json_schema_extra={"example": "VIP"},
    )
    payment_details: str = Field(
        ...,
        description="Encrypted payment information or payment token",
        json_schema_extra={"example": "tok_1JX9Z2KZJZJZJZJZJZJZJZJZ"},
    )
    customer_ip: str = Field(
        ...,
        description="IP address of the customer for fraud detection",
        json_schema_extra={"example": "192.168.1.1"},
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_email": "customer@example.com",
                "customer_id": 12345,
                "showtime_id": 789,
                "seat_list_id": [101, 102, 103],
                "payment_method": "credit_card",
                "ticket_type": "VIP",
                "payment_details": "tok_1JX9Z2KZJZJZJZJZJZJZJZJZ",
                "customer_ip": "192.168.1.1",
            }
        }
    )


class SearchTicketParams(BaseModel):
    """Parameters for searching and filtering tickets with pagination support."""

    movie_id: Optional[int] = Field(
        default=None,
        description="Filter by associated movie ID",
        json_schema_extra={"example": 123},
    )
    showtime_id: Optional[int] = Field(
        default=None,
        description="Filter by showtime ID",
        json_schema_extra={"example": 456},
    )
    user_id: Optional[int] = Field(
        default=None,
        description="Filter by user ID who purchased the tickets",
        json_schema_extra={"example": 789},
    )
    status: Optional[TicketStatus] = Field(
        default=None,
        description="Filter by current ticket status",
        json_schema_extra={"example": "purchased"},
    )
    include_seats: bool = Field(
        default=False, description="Include detailed seat information in the response"
    )
    created_before: Optional[datetime] = Field(
        default=None,
        description="Filter tickets created before this timestamp (ISO 8601 format)",
        json_schema_extra={"example": "2023-12-31T23:59:59Z"},
    )
    created_after: Optional[datetime] = Field(
        default=None,
        description="Filter tickets created after this timestamp (ISO 8601 format)",
        json_schema_extra={"example": "2023-01-01T00:00:00Z"},
    )
    price_min: Optional[float] = Field(
        default=None,
        ge=0,
        description="Minimum ticket price value for filtering",
        json_schema_extra={"example": 10.50},
    )
    price_max: Optional[float] = Field(
        default=None,
        ge=0,
        description="Maximum ticket price value for filtering",
        json_schema_extra={"example": 25.00},
    )
    page_limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of items per page (1-100)",
        json_schema_extra={"example": 20},
    )
    page_offset: int = Field(
        default=0,
        ge=0,
        description="Pagination offset for results",
        json_schema_extra={"example": 0},
    )
    sort_by: str = Field(
        default="created_at",
        description="Field to sort results by (created_at|updated_at|price)",
        json_schema_extra={"example": "price"},
    )
    sort_direction_asc: bool = Field(
        default=True, description="Sort direction (True=ascending, False=descending)"
    )

    @field_validator("price_max")
    @classmethod
    def validate_price_range(cls, v: Optional[float], info):
        """Ensure maximum price is not less than minimum price if both are set."""
        if (
            "price_min" in info.data
            and v is not None
            and info.data["price_min"] is not None
        ):
            if v < info.data["price_min"]:
                raise ValueError("price_max must be greater than or equal to price_min")
        return v

    model_config = ConfigDict(
        use_enum_values=True,
        json_schema_extra={
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
                "sort_direction_asc": False,
            }
        },
    )


class SeatInfo(BaseModel):
    """Detailed information about a specific seat."""

    id: int = Field(
        ..., description="Unique seat identifier", json_schema_extra={"example": 1}
    )
    seat_number: str = Field(
        ...,
        description="Human-readable seat identifier (e.g., 'A12')",
        json_schema_extra={"example": "A12"},
    )
    row: str = Field(
        ...,
        description="Row designation for the seat",
        json_schema_extra={"example": "A"},
    )
    number: int = Field(
        ..., description="Seat number within the row", json_schema_extra={"example": 12}
    )
    type: str = Field(
        ...,
        description="Seat type classification",
        json_schema_extra={"example": "VIP"},
    )


class TicketResponse(BaseModel):
    """Detailed ticket information response DTO."""

    id: int = Field(
        ..., description="Unique ticket identifier", json_schema_extra={"example": 123}
    )
    user_id: int = Field(
        ...,
        description="ID of the user who owns the ticket",
        json_schema_extra={"example": 456},
    )
    movie_id: int = Field(
        ...,
        description="ID of the associated movie",
        json_schema_extra={"example": 789},
    )
    showtime_id: int = Field(
        ...,
        description="ID of the associated showtime",
        json_schema_extra={"example": 101},
    )
    price: float = Field(
        ...,
        description="Price paid for the ticket",
        json_schema_extra={"example": 12.50},
    )
    price_currency: str = Field(
        ...,
        description="Currency code for the ticket price",
        json_schema_extra={"example": "USD"},
    )
    status: TicketStatus = Field(
        ...,
        description="Current status of the ticket",
        json_schema_extra={"example": "purchased"},
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the ticket was created",
        json_schema_extra={"example": "2023-01-01T12:00:00Z"},
    )
    seats: List[SeatInfo] = Field(
        default_factory=list,
        description="List of seats associated with this ticket",
        json_schema_extra={
            "example": [
                {"id": 1, "seat_number": "A12", "row": "A", "number": 12, "type": "VIP"}
            ]
        },
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
                "seats": [
                    {
                        "id": 1,
                        "seat_number": "A12",
                        "row": "A",
                        "number": 12,
                        "type": "VIP",
                    }
                ],
            }
        }
    )


class TicketPurchasedResponse(BaseModel):
    """Response DTO returned after successful ticket purchase."""

    ticket_id: int = Field(
        ...,
        description="Unique identifier of the purchased ticket",
        json_schema_extra={"example": 12345},
    )
    transaction_id: str = Field(
        ...,
        description="Payment processor's transaction reference",
        json_schema_extra={"example": "txn_1JX9Z2KZJZJZJZJZJZJZJZJZ"},
    )
    movie_name: str = Field(
        ...,
        description="Name of the movie booked",
        json_schema_extra={"example": "The Matrix Resurrections"},
    )
    cinema_name: str = Field(
        ...,
        description="Name of the cinema venue",
        json_schema_extra={"example": "Cineplex Downtown"},
    )
    theather_name: str = Field(
        ...,
        description="Name of the movie booked",
        json_schema_extra={"example": "The Matrix Resurrections"},
    )
    showtime_date: datetime = Field(
        ...,
        description="Date and time of the showtime",
        json_schema_extra={"example": "2023-12-25T19:30:00Z"},
    )
    ticket_qr: str = Field(
        ...,
        description="Base64 encoded QR code for ticket validation",
        json_schema_extra={"example": "data:image/png;base64,iVBORw0KGgo..."},
    )
    seats: List[SeatInfo] = Field(
        ...,
        description="List of booked seats with details",
        json_schema_extra={
            "example": [
                {
                    "id": 101,
                    "seat_number": "F12",
                    "row": "F",
                    "number": 12,
                    "type": "Standard",
                }
            ]
        },
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "ticket_id": 12345,
                "transaction_id": "txn_1JX9Z2KZJZJZJZJZJZJZJZJZ",
                "movie_name": "The Matrix Resurrections",
                "cinema_name": "Cineplex Downtown",
                "showtime_date": "2023-12-25T19:30:00Z",
                "ticket_qr": "data:image/png;base64,iVBORw0KGgo...",
                "seats": [
                    {
                        "id": 101,
                        "seat_number": "F12",
                        "row": "F",
                        "number": 12,
                        "type": "Standard",
                    }
                ],
            }
        },
    )


class RefundResponse(BaseModel):
    """Response DTO for ticket refund operations."""

    ticket_id: int = Field(
        ...,
        description="ID of the refunded ticket",
        json_schema_extra={"example": 12345},
    )
    refund_amount: Decimal = Field(
        ...,
        description="Full amount being refunded",
        json_schema_extra={"example": 25.00},
    )
    processing_fee: Decimal = Field(
        ...,
        description="Processing fee deducted from refund",
        json_schema_extra={"example": 2.50},
    )
    net_refund: Decimal = Field(
        ...,
        description="Final amount to be refunded to customer",
        json_schema_extra={"example": 22.50},
    )
    status: str = Field(
        ...,
        description="Current status of the refund",
        json_schema_extra={"example": "processed"},
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "ticket_id": 12345,
                "refund_amount": 25.00,
                "processing_fee": 2.50,
                "net_refund": 22.50,
                "status": "processed",
            }
        }
    )


TicketBuyedResponse = TicketPurchasedResponse
