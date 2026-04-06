from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..exceptions import *
from .combo_items import ComboItem
from .value_objects import ComboId


class Combo(BaseModel):
    """Represents a combo meal consisting of multiple food products."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ComboId
    name: str = Field(..., min_length=1, max_length=200)
    price: Decimal = Field(..., gt=Decimal("0"))
    description: Optional[str] = None
    discount_percentage: Decimal = Field(
        default=Decimal("0"), ge=Decimal("0"), le=Decimal("100")
    )
    image_url: Optional[str] = None
    is_available: bool = True
    items: List[ComboItem] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None

    @field_validator("price", mode="before")
    @classmethod
    def _coerce_price(cls, v):
        if isinstance(v, Decimal):
            return v
        if isinstance(v, str):
            return Decimal(v)
        if isinstance(v, float):
            return Decimal(str(v))
        return Decimal(v)

    @field_validator("discount_percentage", mode="before")
    @classmethod
    def _coerce_discount(cls, v):
        if v is None:
            return Decimal("0")
        if isinstance(v, Decimal):
            return v
        if isinstance(v, str):
            return Decimal(v)
        if isinstance(v, float):
            return Decimal(str(v))
        return Decimal(v)

    def validate_business_logic(self):
        """Validates all business rules for the combo."""
        self._validate_numbers()

    def _validate_numbers(self):
        self._validate_price_range()
        self._validate_item_range()

        product_total_price = self._get_product_total_price_sum()
        self._assert_price(product_total_price)
        self._assert_discount_percentage(product_total_price)

    def _get_product_total_price_sum(self) -> Decimal:
        product_price_sum = Decimal("0")
        for item in self.items:
            item.validate_quantity_range()
            product_price_sum += Decimal(str(item.product.price))
        return product_price_sum

    def _validate_price_range(self):
        min_price = Decimal("1")
        max_price = Decimal("2000")
        if not (min_price <= self.price <= max_price):
            raise PriceRangeException(min_price, max_price)

    def _validate_item_range(self):
        min_items = 1
        max_items = 10
        if not (min_items <= len(self.items) <= max_items):
            raise ItemRangeException(min_items, max_items)

    def _assert_price(self, product_total_price: Decimal):
        if self.price > product_total_price:
            raise PriceSumException(product_total_price)

    def _assert_discount_percentage(self, product_price_sum: Decimal):
        if product_price_sum == Decimal("0"):
            raise DiscountPercentageException(
                Decimal("0"),
                details={
                    "message": "Cannot calculate discount for zero-value product sum"
                },
            )

        combo_price_ratio = (self.price * Decimal("100")) / product_price_sum
        actual_discount = Decimal("100") - combo_price_ratio

    """
    TODO: Fix bug
        tolerance = Decimal("0.01")
        if abs(actual_discount - self.discount_percentage) > tolerance:
            raise DiscountPercentageException(
                round(actual_discount, 2),
                details={
                    "expected": round(float(self.discount_percentage), 2),
                    "actual": round(float(actual_discount), 2),
                    "tolerance": float(tolerance),
                },
            )
    """

    def mark_as_deleted(self):
        self.deleted_at = datetime.now()
        self.is_available = False

    def restore(self):
        self.deleted_at = None
        self.is_available = True
