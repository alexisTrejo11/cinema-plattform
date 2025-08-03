import math
from decimal import Decimal
from typing import Any, Dict
from ..entities.promotion import PromotionId, PromotionType
from app.products.domain.entities.product import Product
from ..entities.valueobjects import PromotionRule, PromotionId


class PercentageDiscountRule(PromotionRule):
    def __init__(
        self,
        flat_percentage_discount: Decimal,
        min_quantity: int = 1,
    ):
        self.min_quantity = min_quantity
        self.flat_percentage_discount = flat_percentage_discount

    @staticmethod
    def create(**kwargs) -> "PromotionRule":
        min_percentage_discount = kwargs.get("min_percentage_discount")
        min_quantity = kwargs.get("min_quantity")

        if not isinstance(min_quantity, int) or min_quantity < 1:
            raise ValueError("min_quantity must be a positive integer.")

        if min_percentage_discount is None:
            raise ValueError("min_percentage_discount is required.")

        if isinstance(min_percentage_discount, str):
            try:
                min_percentage_discount = Decimal(min_percentage_discount)
            except ValueError:
                raise ValueError(
                    "min_percentage_discount must be a valid decimal string."
                )

        if not isinstance(min_percentage_discount, Decimal):
            raise ValueError(
                f"min_percentage_discount must be a Decimal instance. Got {type(min_percentage_discount)}."
            )

        rule = PercentageDiscountRule(
            min_quantity=min_quantity,
            flat_percentage_discount=min_percentage_discount,
        )
        rule.validate()
        return rule

    def apply(self, product: Product) -> Decimal:
        return product.price * (self.flat_percentage_discount / Decimal("100.00"))

    def validate(self) -> None:
        if not (0 <= self.flat_percentage_discount <= Decimal("100.00")):
            raise ValueError("Percentage discount must be between 0 and 100.")

    def to_dict(self) -> dict:
        return {
            "flat_percentage_discount": str(self.flat_percentage_discount),
        }

    def from_dict(self, data: dict) -> "PromotionRule":
        flat_percentage_discount = Decimal(data["flat_percentage_discount"])
        return PercentageDiscountRule(
            flat_percentage_discount=flat_percentage_discount,
        )


class BuyXGetYFreeRule(PromotionRule):
    def __init__(self, buy_quantity: int, get_quantity: int):
        self.buy_quantity = buy_quantity
        self.get_quantity = get_quantity

    @staticmethod
    def create(**kwargs) -> "BuyXGetYFreeRule":
        buy_quantity = kwargs.get("min_quantity")
        get_quantity = kwargs.get("max_quantity")

        if not isinstance(buy_quantity, int):
            raise ValueError("buy_quantity must be an integer.")

        if not isinstance(get_quantity, int):
            raise ValueError("get_quantity must be an integer.")

        rule = BuyXGetYFreeRule(
            buy_quantity=buy_quantity,
            get_quantity=get_quantity,
        )

        rule.validate()
        return rule

    def apply(self, product: Product) -> Decimal:
        return product.price * self.buy_quantity

    def validate(self) -> None:
        MAX_ITEMS_ALLOWED = 12

        if self.buy_quantity <= 0 or self.get_quantity <= 0:
            raise ValueError("Buy and get quantities must be greater than zero.")

        items_quantity_to_pay = self.buy_quantity
        items_quantity_to_get = self.get_quantity

        if items_quantity_to_get > MAX_ITEMS_ALLOWED:
            raise ValueError(
                f"Items to get cannot exceed {MAX_ITEMS_ALLOWED} for buy X get Y promotions."
            )

        min_required_items_to_pay = int(math.ceil(items_quantity_to_get / 2))

        if items_quantity_to_pay < min_required_items_to_pay:
            raise ValueError(
                f"Min Quantity must be at least {min_required_items_to_pay}"
            )

    def to_dict(self) -> dict:
        return {
            "buy_quantity": self.buy_quantity,
            "get_quantity": self.get_quantity,
        }

    def from_dict(self, data: dict) -> "PromotionRule":
        buy_quantity = data["buy_quantity"]
        get_quantity = data["get_quantity"]
        return BuyXGetYFreeRule(
            buy_quantity=buy_quantity,
            get_quantity=get_quantity,
        )


class BundleDiscountRule(PromotionRule):
    def __init__(
        self,
        min_percentage_discount: Decimal,
        max_percentage_discount: Decimal,
        min_quantity: int,
        max_quantity: int,
    ) -> None:
        self.min_bundle_discount = min_percentage_discount
        self.max_bundle_discount = max_percentage_discount
        self.min_bundle_quantity = min_quantity
        self.max_bundle_quantity = max_quantity

    def validate(self) -> None:
        """Validate the bundle discount rule fields."""
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

    def to_dict(self) -> dict:
        """Convert the BundleDiscountRule to a dictionary."""
        return {
            "min_bundle_discount": str(self.min_bundle_discount),
            "max_bundle_discount": str(self.max_bundle_discount),
            "min_bundle_quantity": self.min_bundle_quantity,
            "max_bundle_quantity": self.max_bundle_quantity,
        }

    @staticmethod
    def create(**kwargs) -> "BundleDiscountRule":
        min_bundle_discount = kwargs.get("min_percentage_discount")
        max_bundle_discount = kwargs.get("max_percentage_discount")
        min_bundle_quantity = kwargs.get("min_quantity")
        max_bundle_quantity = kwargs.get("max_quantity")

        if not isinstance(min_bundle_discount, Decimal):
            raise ValueError("min_bundle_discount must be a Decimal instance.")

        if not isinstance(max_bundle_discount, Decimal):
            raise ValueError("max_bundle_discount must be a Decimal instance.")

        if not isinstance(min_bundle_quantity, int):
            raise ValueError("min_bundle_quantity must be an integer.")

        if not isinstance(max_bundle_quantity, int):
            raise ValueError("max_bundle_quantity must be an integer.")

        rule = BundleDiscountRule(
            min_percentage_discount=min_bundle_discount,
            max_percentage_discount=max_bundle_discount,
            min_quantity=min_bundle_quantity,
            max_quantity=max_bundle_quantity,
        )

        rule.validate()
        return rule

    def apply(self, product: Product) -> Decimal:
        """Apply the bundle discount to the product."""
        if self.min_bundle_quantity <= 0 or self.max_bundle_quantity <= 0:
            raise ValueError("Bundle quantities must be greater than zero.")

        if self.min_bundle_discount < Decimal(
            "0.00"
        ) or self.max_bundle_discount < Decimal("0.00"):
            raise ValueError("Bundle discounts cannot be negative.")

        # Assuming the product price is the base price for the bundle
        return product.price * (self.min_bundle_discount / Decimal("100.00"))

    def from_dict(self, data: dict) -> "BundleDiscountRule":
        min_percentage_discount = Decimal(data["min_percentage_discount"])
        max_percentage_discount = Decimal(data["max_percentage_discount"])
        min_quantity = data["min_quantity"]
        max_quantity = data["max_quantity"]

        return BundleDiscountRule(
            min_percentage_discount=min_percentage_discount,
            max_percentage_discount=max_percentage_discount,
            min_quantity=min_quantity,
            max_quantity=max_quantity,
        )


class MinimumQuantityDiscountRule(PromotionRule):
    def __init__(
        self,
        min_quantity: int,
        max_quantity: int,
        min_percentage_discount: Decimal,
        max_percentage_discount: Decimal,
    ) -> None:
        self.min_quantity = min_quantity
        self.max_quantity = max_quantity
        self.min_percentage_discount = min_percentage_discount
        self.max_percentage_discount = max_percentage_discount

    @staticmethod
    def create(**kwargs) -> "MinimumQuantityDiscountRule":
        min_quantity = kwargs.get("min_quantity")
        max_quantity = kwargs.get("max_quantity")
        min_percentage_discount = kwargs.get("min_percentage_discount")
        max_percentage_discount = kwargs.get("max_percentage_discount")

        if not isinstance(min_quantity, int):
            raise ValueError("min_quantity must be an integer.")

        if not isinstance(max_quantity, int):
            raise ValueError("max_quantity must be an integer.")

        if not isinstance(min_percentage_discount, Decimal):
            raise ValueError("min_percentage_discount must be a Decimal instance.")

        if not isinstance(max_percentage_discount, Decimal):
            raise ValueError("max_percentage_discount must be a Decimal instance.")

        rule = MinimumQuantityDiscountRule(
            min_quantity=min_quantity,
            max_quantity=max_quantity,
            min_percentage_discount=min_percentage_discount,
            max_percentage_discount=max_percentage_discount,
        )
        rule.validate()
        return rule

    def apply(self, product: Product) -> Decimal:
        return product.price * (self.min_percentage_discount / Decimal("100.00"))

    def from_dict(self, data: dict) -> "MinimumQuantityDiscountRule":
        min_quantity = data["min_quantity"]
        max_quantity = data["max_quantity"]
        min_percentage_discount = Decimal(data["min_percentage_discount"])
        max_percentage_discount = Decimal(data["max_percentage_discount"])

        return MinimumQuantityDiscountRule(
            min_quantity=min_quantity,
            max_quantity=max_quantity,
            min_percentage_discount=min_percentage_discount,
            max_percentage_discount=max_percentage_discount,
        )

    def validate(self) -> None:
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

    def to_dict(self) -> dict:
        return {
            "min_quantity": self.min_quantity,
            "max_quantity": self.max_quantity,
            "min_percentage_discount": str(self.min_percentage_discount),
            "max_percentage_discount": str(self.max_percentage_discount),
        }


class PromotionRuleFactory:
    @classmethod
    def create_promotion_rule(
        cls,
        promotion_type: PromotionType,
        rule_data: Dict[str, Any],
    ) -> PromotionRule:
        match promotion_type:
            case PromotionType.PERCENTAGE_DISCOUNT:
                return PercentageDiscountRule.create(**rule_data)
            case PromotionType.MINIMUM_QUANTITY_DISCOUNT:
                return MinimumQuantityDiscountRule.create(**rule_data)
            case PromotionType.BUY_X_GET_Y_FREE:
                return BuyXGetYFreeRule.create(**rule_data)
            case PromotionType.BUNDLE_DISCOUNT:
                return BundleDiscountRule.create(**rule_data)
            case _:
                raise ValueError(f"Unsupported promotion type: {promotion.type}")
