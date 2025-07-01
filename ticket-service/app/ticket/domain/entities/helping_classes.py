from datetime import datetime
from decimal import Decimal
from typing import Optional

class CustomerDetails:
    def __init__(self, id: Optional[int] = None) -> None:
        self.id: Optional[int] = id
        self.is_anonymus_user = True
        self.customer_ip_address = None
        
class PriceDetails:
    def __init__(self, price: Decimal, currency: str) -> None:
        self.price = price
        self.currency = currency

class PaymentDetails:
    def __init__(self, id: int, transaction_id: int, type: str, method: str, currency: str) -> None:
        self.id: Optional[int] = id
        self.type: str = type
        self.transaction_id: int = transaction_id
        self.method : str = method
        self.currency : str = currency