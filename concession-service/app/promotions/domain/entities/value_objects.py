import uuid
from decimal import Decimal
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict
from pydantic_core import core_schema

from app.products.domain.entities.value_objects import ProductId
from app.shared.schema import PydanticUUID


class PromotionId(PydanticUUID):
    """Value object for Promotion ID."""

    pass


class PromotionType(str, Enum):
    """Supported promotion types."""

    PERCENTAGE_DISCOUNT = "PERCENTAGE_DISCOUNT"
    BUY_X_GET_Y_FREE = "BUY_X_GET_Y_FREE"
    BUNDLE_DISCOUNT = "BUNDLE_DISCOUNT"
    MINIMUM_QUANTITY_DISCOUNT = "MINIMUM_QUANTITY_DISCOUNT"


class RulesParams(BaseModel):
    """Validated rule parameters for promotion rules."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    minimum_quantity: Optional[int] = None
    maximum_quantity: Optional[int] = None
    min_discount: Optional[Decimal] = None
    max_discount: Optional[Decimal] = None

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


__all__ = ["PromotionId", "PromotionType", "ProductId", "RulesParams"]
