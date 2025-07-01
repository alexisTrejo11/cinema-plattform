from datetime import datetime
from typing import Optional

class Seat:
    def __init__(self, row: str, number: str, id: Optional[int] = None) -> None:
        self.id: Optional[int] = id
        self.row: str = row
        self.number: str = number
        self.type = ""


class Showtime:
    def __init__(self, id: int, seat: Seat, type: str) -> None:
        self.id: int = id
        self.type: str = type
        self.seat: Seat = seat
        self.start_time: datetime
        

class CustomerDetails:
    def __init__(self, id: Optional[int] = None) -> None:
        self.id: Optional[int] = id
        self.is_anonymus_user = True
        self.customer_ip_address = None
        

class PaymentDetails:
    def __init__(self, id: int, transaction_id: int, type: str, method: str, currency: str) -> None:
        self.id: Optional[int] = id
        self.type: str = type
        self.transaction_id: int = transaction_id
        self.method : str = method
        self.currency : str = currency