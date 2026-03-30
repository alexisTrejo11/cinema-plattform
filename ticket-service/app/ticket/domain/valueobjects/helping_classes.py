from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CustomerDetails(BaseModel):
    model_config = ConfigDict(frozen=False)

    user_email: str
    id: Optional[int] = None
    customer_ip_address: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "customer_ip_address": self.customer_ip_address,
        }


class PriceDetails(BaseModel):
    model_config = ConfigDict(frozen=False)

    price: Decimal
    currency: str

    def to_dict(self) -> dict:
        return {
            "price": str(self.price),
            "currency": self.currency,
        }


class PaymentDetails(BaseModel):
    model_config = ConfigDict(frozen=False)

    id: int
    transaction_id: int
    type: str
    method: str
    currency: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "transaction_id": self.transaction_id,
            "method": self.method,
            "currency": self.currency,
        }
