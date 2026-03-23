import math
from decimal import Decimal
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict, model_validator

from app.products.domain.entities.product import Product

from ..entities.value_objects import PromotionType


def _to_decimal(val: Any) -> Decimal:
    if val is None:
        raise ValueError("Expected a numeric value")
    if isinstance(val, Decimal):
        return val
    if isinstance(val, (int, float)):
        return Decimal(str(val))
    if isinstance(val, str):
        return Decimal(val)
    raise ValueError(f"Cannot convert {type(val)} to Decimal")


class PercentageDiscountRule(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    flat_percentage_discount: Decimal
    min_quantity: int = 1

    @classmethod
    def create(cls, **kwargs) -> "PercentageDiscountRule":
        min_percentage_discount = kwargs.get("min_percentage_discount")
        min_quantity = kwargs.get("min_quantity")

        if not isinstance(min_quantity, int) or min_quantity < 1:
            raise ValueError("min_quantity must be a positive integer.")

        if min_percentage_discount is None:
            raise ValueError("min_percentage_discount is required.")

        min_percentage_discount = _to_decimal(min_percentage_discount)

        rule = cls(
            min_quantity=min_quantity,
            flat_percentage_discount=min_percentage_discount,
        )
        rule._validate_rule()
        return rule

    def _validate_rule(self) -> None:
        if not (0 <= self.flat_percentage_discount <= Decimal("100.00")):
            raise ValueError("Percentage discount must be between 0 and 100.")

    def apply(self, product: Product) -> Decimal:
        return product.price * (self.flat_percentage_discount / Decimal("100.00"))


class BuyXGetYFreeRule(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    buy_quantity: int
    get_quantity: int

    @classmethod
    def create(cls, **kwargs) -> "BuyXGetYFreeRule":
        buy_quantity = kwargs.get("min_quantity")
        get_quantity = kwargs.get("max_quantity")

        if not isinstance(buy_quantity, int):
            raise ValueError("buy_quantity must be an integer.")

        if not isinstance(get_quantity, int):
            raise ValueError("get_quantity must be an integer.")

        rule = cls(buy_quantity=buy_quantity, get_quantity=get_quantity)
        rule._validate_rule()
        return rule

    def _validate_rule(self) -> None:
        MAX_ITEMS_ALLOWED = 12

        if self.buy_quantity <= 0 or self.get_quantity <= 0:
            raise ValueError("Buy and get quantities must be greater than zero.")

        if self.get_quantity > MAX_ITEMS_ALLOWED:
            raise ValueError(
                f"Items to get cannot exceed {MAX_ITEMS_ALLOWED} for buy X get Y promotions."
            )

        min_required_items_to_pay = int(math.ceil(self.get_quantity / 2))

        if self.buy_quantity < min_required_items_to_pay:
            raise ValueError(
                f"Min Quantity must be at least {min_required_items_to_pay}"
            )

    def apply(self, product: Product) -> Decimal:
        return product.price * self.buy_quantity


class BundleDiscountRule(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    min_bundle_discount: Decimal
    max_bundle_discount: Decimal
    min_bundle_quantity: int
    max_bundle_quantity: int

    @model_validator(mode="after")
    def _validate_bundle(self) -> "BundleDiscountRule":
        BASE_BUNDLE_DISCOUNT = Decimal("10.00")
        BASE_BUNDLE_QUANTITY = 10

        bundle_quantity_discount_map = {
            BASE_BUNDLE_QUANTITY: BASE_BUNDLE_DISCOUNT,
            25: BASE_BUNDLE_DISCOUNT + Decimal("10.00"),
            40: BASE_BUNDLE_DISCOUNT + Decimal("10.00"),
            60: BASE_BUNDLE_DISCOUNT + Decimal("15.00"),
            80: BASE_BUNDLE_DISCOUNT + Decimal("15.00"),
        }

        if self.min_bundle_quantity not in bundle_quantity_discount_map:
            raise ValueError(
                f"Minimum bundle quantity must be one of {list(bundle_quantity_discount_map.keys())}"
            )

        if self.max_bundle_quantity not in bundle_quantity_discount_map:
            raise ValueError(
                f"Maximum bundle quantity must be one of {list(bundle_quantity_discount_map.keys())}"
            )

        if (
            self.min_bundle_discount
            != bundle_quantity_discount_map[self.min_bundle_quantity]
        ):
            raise ValueError(
                f"Minimum bundle discount must be {bundle_quantity_discount_map[self.min_bundle_quantity]} for {self.min_bundle_quantity} items"
            )

        if (
            self.max_bundle_discount
            != bundle_quantity_discount_map[self.max_bundle_quantity]
        ):
            raise ValueError(
                f"Maximum bundle discount must be {bundle_quantity_discount_map[self.max_bundle_quantity]} for {self.max_bundle_quantity} items"
            )
        return self

    @classmethod
    def create(cls, **kwargs) -> "BundleDiscountRule":
        min_bundle_discount = kwargs.get("min_percentage_discount")
        max_bundle_discount = kwargs.get("max_percentage_discount")
        min_bundle_quantity = kwargs.get("min_quantity")
        max_bundle_quantity = kwargs.get("max_quantity")

        min_bundle_discount = _to_decimal(min_bundle_discount)
        max_bundle_discount = _to_decimal(max_bundle_discount)

        if not isinstance(min_bundle_quantity, int):
            raise ValueError("min_bundle_quantity must be an integer.")

        if not isinstance(max_bundle_quantity, int):
            raise ValueError("max_bundle_quantity must be an integer.")

        return cls(
            min_bundle_discount=min_bundle_discount,
            max_bundle_discount=max_bundle_discount,
            min_bundle_quantity=min_bundle_quantity,
            max_bundle_quantity=max_bundle_quantity,
        )

    def apply(self, product: Product) -> Decimal:
        if self.min_bundle_quantity <= 0 or self.max_bundle_quantity <= 0:
            raise ValueError("Bundle quantities must be greater than zero.")

        if self.min_bundle_discount < Decimal("0.00") or self.max_bundle_discount < Decimal(
            "0.00"
        ):
            raise ValueError("Bundle discounts cannot be negative.")

        return product.price * (self.min_bundle_discount / Decimal("100.00"))


class MinimumQuantityDiscountRule(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    min_quantity: int
    max_quantity: int
    min_percentage_discount: Decimal
    max_percentage_discount: Decimal

    @classmethod
    def create(cls, **kwargs) -> "MinimumQuantityDiscountRule":
        min_quantity = kwargs.get("min_quantity")
        max_quantity = kwargs.get("max_quantity")
        min_percentage_discount = kwargs.get("min_percentage_discount")
        max_percentage_discount = kwargs.get("max_percentage_discount")

        if not isinstance(min_quantity, int):
            raise ValueError("min_quantity must be an integer.")

        if not isinstance(max_quantity, int):
            raise ValueError("max_quantity must be an integer.")

        rule = cls(
            min_quantity=min_quantity,
            max_quantity=max_quantity,
            min_percentage_discount=_to_decimal(min_percentage_discount),
            max_percentage_discount=_to_decimal(max_percentage_discount),
        )
        rule._validate_rule()
        return rule

    def _validate_rule(self) -> None:
        MIN_QUANTITY_ALLOWED = 5
        MAX_QUANTITY_ALLOWED = 100
        BASE_DISCOUNT_PERCENTAGE = 5
        max_percentage_discount_PERCENTAGE = 70

        if self.min_quantity < MIN_QUANTITY_ALLOWED:
            raise ValueError(
                f"this promotion type requires at least {MIN_QUANTITY_ALLOWED} items"
            )

        if self.max_quantity > MAX_QUANTITY_ALLOWED:
            raise ValueError(
                f"this promotion type requires at most {MAX_QUANTITY_ALLOWED} items"
            )

        if self.min_percentage_discount < BASE_DISCOUNT_PERCENTAGE:
            raise ValueError(
                f"min percentage must be higher than {BASE_DISCOUNT_PERCENTAGE}"
            )

        if self.min_percentage_discount < max_percentage_discount_PERCENTAGE:
            raise ValueError(
                f"min percentage must be higher than {BASE_DISCOUNT_PERCENTAGE}"
            )

    def apply(self, product: Product) -> Decimal:
        return product.price * (self.min_percentage_discount / Decimal("100.00"))


class PromotionRuleFactory:
    @classmethod
    def create_promotion_rule(
        cls,
        promotion_type: PromotionType,
        rule_data: Dict[str, Any],
    ) -> dict:
        match promotion_type:
            case PromotionType.PERCENTAGE_DISCOUNT:
                return PercentageDiscountRule.create(**rule_data).model_dump(mode="json")
            case PromotionType.MINIMUM_QUANTITY_DISCOUNT:
                return MinimumQuantityDiscountRule.create(**rule_data).model_dump(
                    mode="json"
                )
            case PromotionType.BUY_X_GET_Y_FREE:
                return BuyXGetYFreeRule.create(**rule_data).model_dump(mode="json")
            case PromotionType.BUNDLE_DISCOUNT:
                return BundleDiscountRule.create(**rule_data).model_dump(mode="json")
            case _:
                raise ValueError(f"Unsupported promotion type: {promotion_type!r}")
