from dataclasses import asdict, dataclass, field
from decimal import Decimal
from typing import List, Optional, Any
from app.shared.schema import AbstractId
import uuid
from enum import Enum, auto
from app.products.domain.entities.value_objects import ProductId
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


class PromotionId(AbstractId):
    """Value object for Promotion ID."""

    def __init__(self, value: uuid.UUID):
        super().__init__(value)

    def __str__(self):
        return str(self.value)

    @staticmethod
    def from_string(value: str) -> "PromotionId":
        """Create a PromotionId from a string."""
        return PromotionId(AbstractId.from_string(value).value)

    @staticmethod
    def generate() -> "PromotionId":
        """Generate a new PromotionId."""
        return PromotionId(AbstractId.generate().value)

    @classmethod
    def _validate(cls, value: Any) -> "PromotionId":
        """Validate input and convert to PromotionId."""
        if isinstance(value, cls):
            return value
        elif isinstance(value, str):
            return cls.from_string(value)
        elif isinstance(value, uuid.UUID):
            return cls(value)
        else:
            raise ValueError(f"Cannot convert {type(value)} to PromotionId")

    class Config:
        orm_mode = True
        json_encoders = {"PromotionId": lambda v: str(v.value)}


class PromotionType(str, Enum):
    """Tipos de promociones soportados por el sistema"""

    PERCENTAGE_DISCOUNT = "PERCENTAGE_DISCOUNT"
    FIXED_DISCOUNT = "FIXED_DISCOUNT"
    BUY_X_GET_Y_FREE = "BUY_X_GET_Y_FREE"
    BUNDLE_DISCOUNT = "BUNDLE_DISCOUNT"
    MINIMUM_QUANTITY_DISCOUNT = "MINIMUM_QUANTITY_DISCOUNT"


@dataclass(frozen=True)
class PromotionRule:
    """Value Object que representa una regla de promoción"""

    # Quantity
    quantity: int = 0
    purchase_amount: Decimal = Decimal("0.00")
    required_products: List[ProductId] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert the PromotionRule to a dictionary."""
        self_dict = asdict(self)
        self_dict["required_products"] = [
            pid.value for pid in self_dict["required_products"]
        ]
        return self_dict

    @classmethod
    def from_dict(cls, data: dict) -> "PromotionRule":
        """Creates a PromotionRule instance from a dictionary representation"""
        return cls(
            quantity=data.get("quantity", 0),
            purchase_amount=(Decimal(data["purchase_amount"])),
            required_products=(
                [ProductId.from_string(pid) for pid in data["required_products"]]
            ),
        )
