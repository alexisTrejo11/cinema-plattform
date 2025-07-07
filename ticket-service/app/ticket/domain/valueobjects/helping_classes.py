from datetime import datetime
from decimal import Decimal
from typing import Optional

class CustomerDetails:
    def __init__(self, user_email: str, id: Optional[int] = None, customer_ip: Optional[str] = None) -> None:
        self.id: Optional[int] = id
        self.user_email: str = user_email
        self.customer_ip_address = customer_ip
    
        
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "customer_ip_address": self.customer_ip_address
        }
        
class PriceDetails:
    def __init__(self, price: Decimal, currency: str) -> None:
        self.price = price
        self.currency = currency
        
        def to_dict(self) -> dict:
            return {
                "price": str(self.price),
                "currency": self.currency
            }
            

class PaymentDetails:
    def __init__(self, id: int, transaction_id: int, type: str, method: str, currency: str) -> None:
        self.id: int = id
        self.type: str = type
        self.transaction_id: int = transaction_id
        self.method : str = method
        self.currency : str = currency
        
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "transaction_id": self.transaction_id,
            "method": self.method,
            "currency": self.currency
        }