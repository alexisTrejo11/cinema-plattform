from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from app.showtime.domain.entities.showtime import Showtime
from app.showtime.domain.entities.theather_seat import TheaterSeat as Seat
from ..valueobjects.helping_classes import CustomerDetails, PaymentDetails, PriceDetails
from ..valueobjects.enums import TicketStatus


class Ticket:
    def __init__(
        self,
        seat : Seat,
        showtime : Showtime,
        price_details: PriceDetails,
        customer_details: Optional[CustomerDetails] = None,
        payment_details: Optional[PaymentDetails] = None,
        status: TicketStatus = TicketStatus.AVAILABLE,
        id: int = 0,
        reservation_time: Optional[datetime] = None,
        confirmation_time: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> None:
        self.id = id
        self.showtime = showtime
        self.price_details = price_details
        self.seat = seat
        self.customer_details = customer_details
        self.status : TicketStatus = status
        self.reservation_time = reservation_time
        self.confirmation_time = confirmation_time
        self.payment_details = payment_details
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def invalid_ticket(self):
        if self.payment_details:
            self.status = TicketStatus.NOT_BUY
        else:
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
    
    def is_refundable(self, showtime_start: datetime) -> bool:
        return True
    
    def calculate_refund_amount(self) -> Decimal:
        return self.showtime.get_price()