from dataclasses import asdict, dataclass, field
from decimal import Decimal
from typing import Optional, Any
from app.products.domain.entities.product import Product
from app.shared.schema import AbstractId
import uuid
from enum import Enum
from app.products.domain.entities.value_objects import ProductId
from abc import ABC, abstractmethod


class PromotionId(AbstractId):
    """Value object for Promotion ID."""

    def __init__(self, value: Any):
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
    BUY_X_GET_Y_FREE = "BUY_X_GET_Y_FREE"
    BUNDLE_DISCOUNT = "BUNDLE_DISCOUNT"
    MINIMUM_QUANTITY_DISCOUNT = "MINIMUM_QUANTITY_DISCOUNT"


class RulesParams:
    def __init__(self, **kwargs):
        self.minimum_quantity: Optional[int] = kwargs.get("minimum_quantity")
        self.maximum_quantity: Optional[int] = kwargs.get("maximum_quantity")
        self.min_discount: Optional[Decimal] = kwargs.get("min_discount")
        self.max_discount: Optional[Decimal] = kwargs.get("max_discount")

    def validate(self, promotion_type: PromotionType) -> None:
        if self.minimum_quantity is not None and self.minimum_quantity < 1:
            raise ValueError("Minimum quantity must be at least 1")
        if self.maximum_quantity is not None and self.maximum_quantity < 1:
            raise ValueError("Maximum quantity must be at least 1")
        if self.min_discount is not None and self.min_discount < Decimal("0"):
            raise ValueError("Minimum discount cannot be negative")
        if self.max_discount is not None and self.max_discount < Decimal("0"):
            raise ValueError("Maximum discount cannot be negative")

        if promotion_type == PromotionType.BUY_X_GET_Y_FREE:
            if self.minimum_quantity is None or self.minimum_quantity < 1:
                raise ValueError("Minimum quantity is required for BUY_X_GET_Y_FREE")
            if (
                self.maximum_quantity is not None
                and self.maximum_quantity < self.minimum_quantity
            ):
                raise ValueError(
                    "Maximum quantity cannot be less than minimum quantity"
                )

        if promotion_type == PromotionType.BUNDLE_DISCOUNT:
            if self.min_discount is None or self.min_discount < Decimal("0"):
                raise ValueError("Minimum discount is required for BUNDLE_DISCOUNT")
            if self.max_discount is not None and self.max_discount < self.min_discount:
                raise ValueError(
                    "Maximum discount cannot be less than minimum discount"
                )

        if promotion_type == PromotionType.MINIMUM_QUANTITY_DISCOUNT:
            if self.minimum_quantity is None or self.minimum_quantity < 1:
                raise ValueError(
                    "Minimum quantity is required for MINIMUM_QUANTITY_DISCOUNT"
                )

        if promotion_type == PromotionType.PERCENTAGE_DISCOUNT:
            if self.min_discount is None or self.min_discount < Decimal("0"):
                raise ValueError("Minimum discount is required for PERCENTAGE_DISCOUNT")


class PromotionRule(ABC):
    @abstractmethod
    def apply(self, product: Product) -> Decimal:
        pass

    @abstractmethod
    def validate(self) -> None:
        """Validate the promotion rule fields."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Convert the PromotionRule to a dictionary."""
        pass

    @abstractmethod
    def from_dict(self, data: dict) -> "PromotionRule":
        """Convert a dictionary to a PromotionRule."""
        pass
