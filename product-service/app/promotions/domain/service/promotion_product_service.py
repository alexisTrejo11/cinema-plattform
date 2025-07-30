from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
from ..valueobjects import PromotionId, PromotionType, PromotionRule, ProductId
from app.shared.base_exceptions import DomainException
from ..promotion import Promotion
from app.products.domain.entities.product import Product


# TODO: Refactor with strategy pattern
class PromotionProductService:
    @classmethod
    def get_promotion_discount(
        cls, promotion: Promotion, products_to_claim: List[Product]
    ) -> Decimal:
        cls.assert_promotion_is_active(promotion)

        # Calculate the discount applied of the requested products. Could be less than the total in rule
        discount = cls._calculate_discount_from_products(promotion, products_to_claim)

        return Decimal(discount)

    @classmethod
    def validate_promotion_rule_creation(
        cls, promotion: Promotion, products_required_in_rule: List[Product]
    ) -> Optional[PromotionRule]:
        cls.assert_promotion_is_active(promotion)
        cls.assert_same_products(promotion, products_required_in_rule)

        rule = promotion.rule
        prices_allowed_buy_x_yet_free = []
        product_total_sum = Decimal("0.00")

        for product in products_required_in_rule:
            product_total_sum += product.price
            prices_allowed_buy_x_yet_free.append(product.price)

        cls.assert_discount_is_less_than_total(promotion, product_total_sum)

        # Calculate the discount applied of the all of products required
        purchase_discount = (
            rule.purchase_amount * Decimal("100.00")
        ) / product_total_sum
        discount_applied = 100 - purchase_discount

        cls.validate_promotion_type_creation(
            promotion,
            discount_applied,
            product_total_sum,
            prices_allowed_buy_x_yet_free,
        )

    @classmethod
    def validate_flat_discount(
        cls, promotion: Promotion, discount_applied: Decimal
    ) -> None:
        MIN_PERCENTAGE_DISCOUNT = 10
        MAX_PERCENTAGE_DISCOUNT = 90

        if not MIN_PERCENTAGE_DISCOUNT <= discount_applied <= MAX_PERCENTAGE_DISCOUNT:
            raise DomainException(
                f"""
                    For this Promotion type {promotion.promotion_type} the allowed disccount range is
                    {MIN_PERCENTAGE_DISCOUNT}%  to {MAX_PERCENTAGE_DISCOUNT}% 
                    and requested percentage is
                    {discount_applied}%
                    """
            )

    @classmethod
    def validate_promotion_buy_x_get_yet_free(
        cls, prices_allowed_buy_x_yet_free: List[Decimal], promotion: Promotion
    ) -> None:
        rule = promotion.rule
        QUANTITY_EXTRA_ITEMS = 3

        extra_items_claimed = abs(rule.quantity - len(rule.required_products))

        if extra_items_claimed > QUANTITY_EXTRA_ITEMS:
            raise DomainException("For this Promotion type only 3 items can be claimed")

        # Check last 3 elements in prices if there are more or equal than 4
        if len(prices_allowed_buy_x_yet_free) >= 4:
            last_3_prices = prices_allowed_buy_x_yet_free[-3:]
            if promotion.discount_value not in last_3_prices:
                cls.raise_promotion_not_applicable_exception(
                    f"The allowed prices are {prices_allowed_buy_x_yet_free[-3:]}"
                )

        # Check in all prices becase there are less than 4 (No array pointer conflict)
        if promotion.discount_value not in prices_allowed_buy_x_yet_free:
            cls.raise_promotion_not_applicable_exception(
                f"The allowed prices are {prices_allowed_buy_x_yet_free}"
            )

    @classmethod
    def validate_promotion_fixed_discount(cls, discount_applied: Decimal) -> None:
        MAX_FIXED_DISCOUNT_ALLOWED = 30  # Allow Max 30%

        if discount_applied > MAX_FIXED_DISCOUNT_ALLOWED:
            cls.raise_promotion_not_applicable_exception(
                f"For this Promotion type the max allowed disccount are {MAX_FIXED_DISCOUNT_ALLOWED}%"
                + f" and requested percentage is {discount_applied}%"
            )

    @classmethod
    def validate_promotion_bundle_discount(
        cls, rule: PromotionRule, discount_applied: Decimal
    ) -> None:
        MIN_BUNDLE_QUANTITY = 2
        MAX_BUNDLE_DISCOUNT_ALLOWED = 50  # Allow Max 50% IN BUNDLE PROMOTION
        if rule.quantity < MIN_BUNDLE_QUANTITY:
            cls.raise_promotion_not_applicable_exception(
                f"""Bundle must have at least 2 items to be valid."""
            )
        if discount_applied > MAX_BUNDLE_DISCOUNT_ALLOWED:
            cls.raise_promotion_not_applicable_exception(
                f"""Max allowed disccount are {MAX_BUNDLE_DISCOUNT_ALLOWED}% and
                requested percentage is {discount_applied}%"""
            )

    @classmethod
    def validate_promotion_minimum_quantity_discount(
        cls, rule: PromotionRule, discount_applied: Decimal, product_total_sum: Decimal
    ) -> None:
        QUANTITY_ITEMS_REQUIRED = 5
        PERCENTAGE_TO_APPLY = 10  # Starts on 10%. Every 5 products increase 10%
        MAX_PERCENTAGE_ALLOWED = 60  # Ends on 60%. Max percentage allowed

        if len(rule.required_products) < QUANTITY_ITEMS_REQUIRED:
            raise DomainException("At least 5 item are required")

        extra_items = len(rule.required_products) - QUANTITY_ITEMS_REQUIRED

        # Apply custom discount
        while extra_items > 0:
            if PERCENTAGE_TO_APPLY >= MAX_PERCENTAGE_ALLOWED:
                break
            extra_items -= 5
            PERCENTAGE_TO_APPLY += 10

        quantity_required = (product_total_sum * PERCENTAGE_TO_APPLY) / 100
        if discount_applied != PERCENTAGE_TO_APPLY:
            cls.raise_promotion_not_applicable_exception(
                f"""Max allowed discount are {PERCENTAGE_TO_APPLY}% 
                and requested percentage is {discount_applied}% 
                quantity_required {quantity_required} 
                quantity_provided {discount_applied}"""
            )

    @classmethod
    def assert_promotion_is_active(cls, promotion: Promotion) -> None:
        if not promotion.is_active:
            raise DomainException("The promotion is not active")

        if datetime.now() < promotion.start_date or datetime.now() > promotion.end_date:
            raise DomainException("The promotion is not currently valid")

    @classmethod
    def assert_discount_is_less_than_total(
        cls, promotion: Promotion, product_total: Decimal
    ) -> None:

        if product_total < promotion.discount_value:
            raise DomainException(
                "Total purchase amount does not meet the minimum requirement for the promotion"
            )

    @classmethod
    def raise_promotion_not_applicable_exception(cls, message: str) -> None:
        raise DomainException(f"For this Promotion type: {message}")

    @classmethod
    def assert_same_products(
        cls, promotion: Promotion, products: List[Product]
    ) -> None:
        if not set(promotion.rule.required_products).intersection(
            [p.id for p in products]
        ):
            raise DomainException(
                "Promotion is not applicable to the provided products"
            )

    @classmethod
    def _calculate_discount_from_products(
        cls, promotion: Promotion, products: List[Product]
    ) -> Decimal:
        if not set(promotion.rule.required_products).intersection(
            [p.id for p in products]
        ):
            raise DomainException(
                "Promotion is not applicable to the provided products"
            )

        product_total_sum = Decimal(sum(product.price for product in products))
        cls.assert_discount_is_less_than_total(promotion, product_total_sum)

        rule = promotion.rule
        if promotion.promotion_type == PromotionType.BUY_X_GET_Y_FREE:
            # Calculate the discount based on the number of products claimed
            extra_items_claimed = abs(len(products) - rule.quantity)
            if extra_items_claimed > 3:
                raise DomainException(
                    "For this Promotion type only 3 items can be claimed"
                )
            return product_total_sum
        else:
            # Calculate the discount applied of the requested products
            purchase_discount = (
                rule.purchase_amount * Decimal("100.00")
            ) / product_total_sum
            discount_applied = 100 - purchase_discount

            return discount_applied

    @classmethod
    def validate_promotion_type_creation(
        cls,
        promotion: Promotion,
        discount_applied: Decimal,
        product_total_sum: Decimal,
        prices_allowed_buy_x_yet_free: List[Decimal] = [],
    ) -> None:

        rule = promotion.rule
        match promotion.promotion_type:
            case PromotionType.BUY_X_GET_Y_FREE:
                cls.validate_promotion_buy_x_get_yet_free(
                    prices_allowed_buy_x_yet_free, promotion
                )
            case PromotionType.FIXED_DISCOUNT:
                cls.validate_promotion_fixed_discount(discount_applied)
            case PromotionType.BUNDLE_DISCOUNT:
                cls.validate_promotion_bundle_discount(rule, discount_applied)
            case PromotionType.MINIMUM_QUANTITY_DISCOUNT:
                cls.validate_promotion_minimum_quantity_discount(
                    rule, discount_applied, product_total_sum
                )
            case _:
                cls.validate_flat_discount(promotion, product_total_sum)
