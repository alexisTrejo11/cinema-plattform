from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import List, Optional
from app.shared.schema import AbstractId
import uuid
from enum import Enum, auto
from app.products.domain.entities.value_objects import ProductId


class PromotionId(AbstractId):
    """Value object for Promotion ID."""

    def __init__(self, value: uuid.UUID):
        super().__init__(value)

    @staticmethod
    def from_string(value: str) -> "PromotionId":
        """Create a PromotionId from a string."""
        return PromotionId(AbstractId.from_string(value).value)

    @staticmethod
    def generate() -> "PromotionId":
        """Generate a new PromotionId."""
        return PromotionId(AbstractId.generate().value)


class PromotionType(Enum):
    """Tipos de promociones soportados por el sistema"""

    PERCENTAGE_DISCOUNT = auto()
    FIXED_DISCOUNT = auto()
    BUY_X_GET_Y_FREE = auto()
    BUNDLE_DISCOUNT = auto()
    MINIMUM_QUANTITY_DISCOUNT = auto()


@dataclass(frozen=True)
class PromotionRule:
    """Value Object que representa una regla de promoción"""

    min_quantity: Optional[int] = None
    min_purchase_amount: Optional[Decimal] = None
    applicable_categories: Optional[List[str]] = None
    required_products: Optional[List[ProductId]] = None

    def to_dict(self) -> dict:
        """Convert the PromotionRule to a dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "PromotionRule":
        """Creates a PromotionRule instance from a dictionary representation"""
        return cls(
            min_quantity=data.get("min_quantity"),
            min_purchase_amount=(
                Decimal(data["min_purchase_amount"])
                if data.get("min_purchase_amount")
                else None
            ),
            applicable_categories=data.get("applicable_categories"),
            required_products=(
                [ProductId.from_string(pid) for pid in data["required_products"]]
                if data.get("required_products")
                else None
            ),
        )
