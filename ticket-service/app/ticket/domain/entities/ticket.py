from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional
from app.seats.domain.showtime_seat import ShowtimeSeat
from ..valueobjects.helping_classes import CustomerDetails, PaymentDetails, PriceDetails
from ..valueobjects.enums import TicketStatus, TicketType


MAX_LIMIT_OF_SEATS_PER_TICKET = 12

class Ticket:
    def __init__(
        self,
        showtime_id : int,
        movie_id : int,
        price_details: PriceDetails,
        ticket_type: TicketType,
        seats : List[ShowtimeSeat] = [],
        customer_details: Optional[CustomerDetails] = None,
        payment_details: Optional[PaymentDetails] = None,
        status: TicketStatus = TicketStatus.RESERVED,
        id: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> None:
        self.id = id
        self.showtime_id = showtime_id
        self.movie_id = movie_id
        self.price_details = price_details
        self.seats = seats if seats else []
        self.customer_details = customer_details
        self.status : TicketStatus = status
        self.ticket_type : TicketType = ticket_type
        self.payment_details = payment_details
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)


    def invalid_ticket(self):
        if self.payment_details:
            self.status = TicketStatus.NOT_USED
            
        self.updated_at = datetime.now(timezone.utc)

    def reserve_ticket(self):
        self.status = TicketStatus.USED
        self.reservation_time = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def cancel_ticket(self) -> None:
        self.status = TicketStatus.CANCELLED
        self.updated_at = datetime.now(timezone.utc)
            
    def use_ticket(self):
        self.status = TicketStatus.USED
        self.updated_at = datetime.now(timezone.utc)
    
    def is_cancelable(self) -> bool:
        return True
    
    
    
    @staticmethod
    def max_seats_allowed_per_ticket() -> int:    
        return MAX_LIMIT_OF_SEATS_PER_TICKET
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "seats": list(seat.to_dict() for seat in self.seats),
            "showtime_id": self.showtime_id,
            "payment_details": dict(self.payment_details.to_dict()) if self.payment_details else None,
            "customer_details": dict(self.customer_details.to_dict()) if self.customer_details else None,
            "price": self.price_details.price,
            "status": self.status.value,
            "reservation_time": self.reservation_time.isoformat() if self.reservation_time else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }