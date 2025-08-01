from abc import ABC, abstractmethod
from decimal import Decimal
from .promotion import PromotionId, PromotionType
from app.products.domain.entities.product import Product
import math


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

    @abstractmethod
    def create(cls, **kwargs) -> "PromotionRule":
        """Create a PromotionRule from a Promotion."""
        pass


class PercentageDiscountRule(PromotionRule):
    def __init__(self, promotion_id: PromotionId, percentage_discount: Decimal):
        self.promotion_id = promotion_id
        self.percentage_discount = percentage_discount

    def create(self, **kwargs) -> "PromotionRule":
        promotion_id = kwargs.get("promotion_id")
        percentage_discount = kwargs.get("percentage_discount")
        if not isinstance(promotion_id, PromotionId):
            raise ValueError("promotion_id must be a PromotionId instance.")

        if not isinstance(percentage_discount, Decimal):
            raise ValueError("percentage_discount must be a Decimal instance.")

        rule = PercentageDiscountRule(
            promotion_id=self.promotion_id,
            percentage_discount=self.percentage_discount,
        )
        rule.validate()
        return rule

    def apply(self, product: Product) -> Decimal:
        return product.price * (self.percentage_discount / Decimal("100.00"))

    def validate(self) -> None:
        if not (0 <= self.percentage_discount <= Decimal("100.00")):
            raise ValueError("Percentage discount must be between 0 and 100.")

    def to_dict(self) -> dict:
        return {
            "promotion_id": str(self.promotion_id),
            "percentage_discount": str(self.percentage_discount),
        }

    def from_dict(self, data: dict) -> "PromotionRule":
        promotion_id = PromotionId.from_string(data["promotion_id"])
        percentage_discount = Decimal(data["percentage_discount"])
        return PercentageDiscountRule(
            promotion_id=promotion_id,
            percentage_discount=percentage_discount,
        )


class BuyXGetYFreeRule(PromotionRule):
    def __init__(self, promotion_id: PromotionId, buy_quantity: int, get_quantity: int):
        self.promotion_id = promotion_id
        self.buy_quantity = buy_quantity
        self.get_quantity = get_quantity

    def create(self, **kwargs) -> "BuyXGetYFreeRule":
        promotion_id = kwargs.get("promotion_id")
        buy_quantity = kwargs.get("buy_quantity")
        get_quantity = kwargs.get("get_quantity")

        if not isinstance(promotion_id, PromotionId):
            raise ValueError("promotion_id must be a PromotionId instance.")

        if not isinstance(buy_quantity, int):
            raise ValueError("buy_quantity must be an integer.")

        if not isinstance(get_quantity, int):
            raise ValueError("get_quantity must be an integer.")

        rule = BuyXGetYFreeRule(
            promotion_id=promotion_id,
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
            "promotion_id": str(self.promotion_id),
            "buy_quantity": self.buy_quantity,
            "get_quantity": self.get_quantity,
        }

    def from_dict(self, data: dict) -> "PromotionRule":
        promotion_id = PromotionId(data["promotion_id"])
        buy_quantity = data["buy_quantity"]
        get_quantity = data["get_quantity"]
        return BuyXGetYFreeRule(
            promotion_id=promotion_id,
            buy_quantity=buy_quantity,
            get_quantity=get_quantity,
        )


class BundleDiscountRule(PromotionRule):
    def __init__(
        self,
        promotion_id: PromotionId,
        min_bundle_discount: Decimal,
        max_bundle_discount: Decimal,
        min_bundle_quantity: int,
        max_bundle_quantity: int,
    ) -> None:
        self.promotion_id = promotion_id
        self.min_bundle_discount = min_bundle_discount
        self.max_bundle_discount = max_bundle_discount
        self.min_bundle_quantity = min_bundle_quantity
        self.max_bundle_quantity = max_bundle_quantity

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
            "promotion_id": str(self.promotion_id),
            "min_bundle_discount": str(self.min_bundle_discount),
            "max_bundle_discount": str(self.max_bundle_discount),
            "min_bundle_quantity": self.min_bundle_quantity,
            "max_bundle_quantity": self.max_bundle_quantity,
        }

    def create(self, **kwargs) -> "BundleDiscountRule":
        promotion_id = kwargs.get("promotion_id")
        min_bundle_discount = kwargs.get("min_bundle_discount")
        max_bundle_discount = kwargs.get("max_bundle_discount")
        min_bundle_quantity = kwargs.get("min_bundle_quantity")
        max_bundle_quantity = kwargs.get("max_bundle_quantity")

        if not isinstance(promotion_id, PromotionId):
            raise ValueError("promotion_id must be a PromotionId instance.")

        if not isinstance(min_bundle_discount, Decimal):
            raise ValueError("min_bundle_discount must be a Decimal instance.")

        if not isinstance(max_bundle_discount, Decimal):
            raise ValueError("max_bundle_discount must be a Decimal instance.")

        if not isinstance(min_bundle_quantity, int):
            raise ValueError("min_bundle_quantity must be an integer.")

        if not isinstance(max_bundle_quantity, int):
            raise ValueError("max_bundle_quantity must be an integer.")

        rule = BundleDiscountRule(
            promotion_id=promotion_id,
            min_bundle_discount=min_bundle_discount,
            max_bundle_discount=max_bundle_discount,
            min_bundle_quantity=min_bundle_quantity,
            max_bundle_quantity=max_bundle_quantity,
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
        promotion_id = PromotionId.from_string(data["promotion_id"])
        min_bundle_discount = Decimal(data["min_bundle_discount"])
        max_bundle_discount = Decimal(data["max_bundle_discount"])
        min_bundle_quantity = data["min_bundle_quantity"]
        max_bundle_quantity = data["max_bundle_quantity"]

        return BundleDiscountRule(
            promotion_id=promotion_id,
            min_bundle_discount=min_bundle_discount,
            max_bundle_discount=max_bundle_discount,
            min_bundle_quantity=min_bundle_quantity,
            max_bundle_quantity=max_bundle_quantity,
        )


class MinimumQuantityDiscountRule(PromotionRule):
    def __init__(
        self,
        promotion_id: PromotionId,
        min_quantity: int,
        max_quantity: int,
        min_percentage_discount: Decimal,
        max_percentage_discount: Decimal,
    ) -> None:
        self.promotion_id = promotion_id
        self.min_quantity = min_quantity
        self.max_quantity = max_quantity
        self.min_percentage_discount = min_percentage_discount
        self.max_percentage_discount = max_percentage_discount

    def create(self, **kwargs) -> "MinimumQuantityDiscountRule":
        rule = MinimumQuantityDiscountRule(
            promotion_id=self.promotion_id,
            min_quantity=self.min_quantity,
            max_quantity=self.max_quantity,
            min_percentage_discount=self.min_percentage_discount,
            max_percentage_discount=self.max_percentage_discount,
        )
        rule.validate()
        return rule

    def apply(self, product: Product) -> Decimal:
        return product.price * (self.min_percentage_discount / Decimal("100.00"))

    def from_dict(self, data: dict) -> "MinimumQuantityDiscountRule":
        promotion_id = PromotionId.from_string(data["promotion_id"])
        min_quantity = data["min_quantity"]
        max_quantity = data["max_quantity"]
        min_percentage_discount = Decimal(data["min_percentage_discount"])
        max_percentage_discount = Decimal(data["max_percentage_discount"])

        return MinimumQuantityDiscountRule(
            promotion_id=promotion_id,
            min_quantity=min_quantity,
            max_quantity=max_quantity,
            min_percentage_discount=min_percentage_discount,
            max_percentage_discount=max_percentage_discount,
        )

    def validate(self) -> None:
        MIN_QUANTITY_ALLOWED = 5
        MAX_QUANTITY_ALLOWED = 100
        BASE_DISCOUNT_PERCENTAGE = 5
        MAX_DISCOUNT_PERCENTAGE = 70

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

        if self.min_percentage_discount < MAX_DISCOUNT_PERCENTAGE:
            raise ValueError(
                f"min percentage must be higher than {BASE_DISCOUNT_PERCENTAGE}"
            )

    def to_dict(self) -> dict:
        return {
            "promotion_id": str(self.promotion_id),
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
        rule_data: dict,
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
