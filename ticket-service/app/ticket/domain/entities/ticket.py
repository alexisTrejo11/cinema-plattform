from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..valueobjects.enums import TicketStatus, TicketType
from ..valueobjects.helping_classes import CustomerDetails, PaymentDetails, PriceDetails
from .seats import ShowtimeSeat

MAX_LIMIT_OF_SEATS_PER_TICKET = 12


class Ticket(BaseModel):
    model_config = ConfigDict(frozen=False)

    showtime_id: int
    movie_id: int
    price_details: PriceDetails
    ticket_type: TicketType
    payment_details: Optional[PaymentDetails] = None
    seats: List[ShowtimeSeat] = Field(default_factory=list)
    customer_details: Optional[CustomerDetails] = None
    status: TicketStatus = TicketStatus.RESERVED
    id: int = 0
    reservation_time: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def invalid_ticket(self) -> None:
        if self.payment_details:
            self.status = TicketStatus.NOT_USED
        self.updated_at = datetime.now(timezone.utc)

    def reserve_ticket(self) -> None:
        self.status = TicketStatus.USED
        self.reservation_time = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def cancel_ticket(self) -> None:
        self.status = TicketStatus.CANCELLED
        self.updated_at = datetime.now(timezone.utc)

    def use_ticket(self) -> None:
        self.status = TicketStatus.USED
        self.updated_at = datetime.now(timezone.utc)

    def is_cancelable(self) -> bool:
        return True

    @staticmethod
    def max_seats_allowed_per_ticket() -> int:
        return MAX_LIMIT_OF_SEATS_PER_TICKET

    def to_dict(self) -> dict:
        user_id = (
            self.customer_details.id
            if self.customer_details and self.customer_details.id is not None
            else 0
        )
        return {
            "id": self.id,
            "user_id": user_id,
            "seats": [s.to_seat_info_dict() for s in self.seats],
            "showtime_id": self.showtime_id,
            "movie_id": self.movie_id,
            "payment_details": (
                dict(self.payment_details.to_dict()) if self.payment_details else None
            ),
            "customer_details": (
                dict(self.customer_details.to_dict()) if self.customer_details else None
            ),
            "price": (
                float(self.price_details.price)
                if isinstance(self.price_details.price, Decimal)
                else self.price_details.price
            ),
            "price_currency": self.price_details.currency,
            "status": self.status,
            "reservation_time": (
                self.reservation_time.isoformat() if self.reservation_time else None
            ),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
