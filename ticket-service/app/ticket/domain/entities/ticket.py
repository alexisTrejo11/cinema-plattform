from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from .helping_classes import Showtime, CustomerDetails, PaymentDetails
from ..valueobjects.enums import TicketStatus
        
class Ticket:
    def __init__(
        self,
        showtime: Showtime,
        price: Decimal,
        currency : str,
        customer_details: CustomerDetails,
        payment_details: Optional[PaymentDetails],
        id: Optional[int] = None,
        status: TicketStatus = TicketStatus.RESERVED,
        reservation_time: Optional[datetime] = None,
        confirmation_time: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> None:
        self.id = id
        self.showtime = showtime
        self.price = price
        self.customer_details = customer_details
        self.status = status
        self.reservation_time = reservation_time
        self.confirmation_time = confirmation_time
        self.currency : str = currency
        self.payment_details = payment_details
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    
    def confirm_ticket(self):
        pass
    
    def cancel_ticket(self):
        pass
    
    def use_ticket(self):
        pass
    
    def is_refundable(self, showtime_start: datetime) -> bool:
        return True
    
    def calculate_refund_amount(self) -> Decimal:
        return Decimal("0.00")