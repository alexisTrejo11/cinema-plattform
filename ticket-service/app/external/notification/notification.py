from typing import List, Optional
from pydantic import BaseModel, EmailStr
from app.internal.ticket.domain.entities.ticket import Ticket


class Notification(BaseModel):
    tickets: List[Ticket]
    customer_email: EmailStr
    customer_id: int
    ticket_qr: str