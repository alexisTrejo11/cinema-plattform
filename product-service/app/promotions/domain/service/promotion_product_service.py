from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from ..valueobjects import PromotionId, PromotionType, PromotionRule, ProductId
from app.shared.base_exceptions import DomainException
from ..promotion import Promotion
from app.products.domain.entities.product import Product


class PromotionProductService:
    # TODO: Check
    @classmethod
    def apply_promotion(cls, promotion: Promotion, products: List[Product]) -> Decimal:
        """
        Applies the promotion to a list of products and returns the calculated discount

        Args:
            products: List of product IDs in the cart

        Returns:
            Total applicable discount amount

        Raises:
            DomainException: If the promotion is not applicable
        """
        if not promotion.is_active:
            raise DomainException("The promotion is not active")

        if datetime.now() < promotion.start_date or datetime.now() > promotion.end_date:
            raise DomainException("The promotion is not currently valid")

        if (
            promotion.max_uses is not None
            and promotion.current_uses >= promotion.max_uses
        ):
            raise DomainException("The promotion has reached its usage limit")

        # Implement specific logic based on promotion type
        discount = Decimal("0")
        applicable_products = [
            p for p in products if p.id in promotion.applicable_product_ids
        ]

        if not applicable_products:
            return Decimal("0")

        # Example implementation for percentage discount
        if promotion.promotion_type == PromotionType.PERCENTAGE_DISCOUNT:
            discount = sum(
                cls.calculate_product_discount(promotion, p)
                for p in applicable_products
            )

        # Other promotion types would be implemented here...

        promotion.current_uses += 1
        promotion.updated_at = datetime.now()
        return discount

    @classmethod
    def validate_promotion_rule_integrity(
        cls, promotion: Promotion, products: List[Product]
    ) -> Optional[PromotionRule]:
        rule = promotion.rule

        if not set(rule.required_products).intersection([p.id for p in products]):
            raise DomainException(
                "Promotion is not applicable to the provided products"
            )

        prices_allowed_buy_x_yet_free = []

        price = Decimal("0.00")
        product_total = sum(product.price for product in products)

        for product in products:
            product_total += price

            price += product.price
            prices_allowed_buy_x_yet_free.append(price)

        if product_total < promotion.discount_value:
            raise DomainException(
                "Total purchase amount does not meet the minimum requirement for the promotion"
            )

        match promotion.promotion_type:
            case PromotionType.BUY_X_GET_Y_FREE:
                prices_allowed_buy_x_yet_free = []

                price = Decimal("0.00")
                for product in products:
                    price += product.price
                    prices_allowed_buy_x_yet_free.append(price)

                if rule.min_quantity - len(promotion.applicable_product_ids) > 3:
                    raise DomainException(
                        "For this Promotion type only 3 items can be claimed"
                    )

                if not len(prices_allowed_buy_x_yet_free) > 4:
                    if promotion.discount_value not in prices_allowed_buy_x_yet_free:
                        raise DomainException(
                            f"""
                        For this Promotion type de allowed 
                        prices are {prices_allowed_buy_x_yet_free}
                        """
                        )
                else:
                    last_3_prices = prices_allowed_buy_x_yet_free[-3]
                    if promotion.discount_value not in last_3_prices:
                        raise DomainException(
                            f"""
                            For this Promotion type de allowed 
                            prices are {prices_allowed_buy_x_yet_free[last_3_prices]}
                            """
                        )
            case PromotionType.FIXED_DISCOUNT:
                MAX_FIXED_DISCOUNT_ALLOWED = 30  # Allow Max 30%
                purchase_disccount = (
                    rule.min_purchase_amount * Decimal("100.00")
                ) / product_total
                purchase_disccount_applied = 100 - purchase_disccount

                if purchase_disccount_applied > MAX_FIXED_DISCOUNT_ALLOWED:
                    raise DomainException(
                        f"""
                            For this Promotion type the max allowed disccount
                            are {MAX_FIXED_DISCOUNT_ALLOWED}% 
                            and requested percentage is
                            {purchase_disccount_applied}%
                            """
                    )
            case PromotionType.BUNDLE_DISCOUNT:
                MIN_BUNDLE_QUANTITY = 2
                MAX_BUNDLE_DISCOUNT_ALLOWED = 50  # Allow Max 50% IN BUNDLE PROMOTION
                if rule.min_quantity < MIN_BUNDLE_QUANTITY:
                    raise DomainException(
                        f"""
                        Bundle must have at least 2 items to be valid.
                        """
                    )
                purchase_disccount = (
                    rule.min_purchase_amount * Decimal("100.00")
                ) / product_total
                purchase_disccount_applied = 100 - purchase_disccount

                if purchase_disccount_applied > MAX_BUNDLE_DISCOUNT_ALLOWED:
                    raise DomainException(
                        f"""
                            For this Promotion type the max allowed disccount
                            are {MAX_BUNDLE_DISCOUNT_ALLOWED}% 
                            and requested percentage is
                            {purchase_disccount_applied}%
                            """
                    )
            case PromotionType.MINIMUM_QUANTITY_DISCOUNT:
                MIN_MINIMUM_QUANTITY_DISCOUNT_QUANTITY = (
                    5  # At least 10 items to apply this promotion are required.
                )
                START_PERCENTAGE = 10  # Every 5 products increate to 10%
                MAX_PERCENTAGE_ALLOWED = 60  # limit

                if len(rule.required_products) < MIN_MINIMUM_QUANTITY_DISCOUNT_QUANTITY:
                    raise DomainException("At least 5 item are required")

                extra_items = (
                    len(rule.required_products) - MIN_MINIMUM_QUANTITY_DISCOUNT_QUANTITY
                )

                # Apply custom disscoount
                while extra_items > 0:
                    if START_PERCENTAGE >= MAX_PERCENTAGE_ALLOWED:
                        break

                    extra_items -= 5
                    START_PERCENTAGE += 10

                PERCENTAGE_TO_APPLY = START_PERCENTAGE

                # Check Disccount
                purchase_disccount = (
                    rule.min_purchase_amount * Decimal("100.00")
                ) / product_total
                purchase_disccount_applied = 100 - purchase_disccount

                quantity_required = (product_total * PERCENTAGE_TO_APPLY) / 100
                if purchase_disccount_applied != PERCENTAGE_TO_APPLY:
                    raise DomainException(
                        f"""
                            For this Promotion type the max allowed disccount
                            are {PERCENTAGE_TO_APPLY}% 
                            and requested percentage is
                            {purchase_disccount_applied}%
                            
                            quantity_required {quantity_required}
                            quantity_provided {purchase_disccount}
                            """
                    )
            case _:  # Default flat percentage disccount
                MIN_PERCENTAGE_DISCOUNT = 10
                MAX_PERCENTAGE_DISCOUNT = 90

                purchase_disccount = (
                    rule.min_purchase_amount * Decimal("100.00")
                ) / product_total
                purchase_disccount_applied = 100 - purchase_disccount

                if (
                    not MIN_PERCENTAGE_DISCOUNT
                    <= purchase_disccount_applied
                    <= MAX_PERCENTAGE_DISCOUNT
                ):
                    raise DomainException(
                        f"""
                            For this Promotion type {promotion.promotion_type} the allowed disccount range is
                            {MIN_PERCENTAGE_DISCOUNT}%  to {MAX_PERCENTAGE_DISCOUNT}% 
                            and requested percentage is
                            {purchase_disccount_applied}%
                            """
                    )

    @classmethod
    def calculate_product_discount(
        cls, promotion: Promotion, product: Product
    ) -> Decimal:

        if promotion.promotion_type == PromotionType.PERCENTAGE_DISCOUNT:
            return product.price * (promotion.discount_value / Decimal("100"))
        elif promotion.promotion_type == PromotionType.FIXED_DISCOUNT:
            return min(promotion.discount_value, product.price)
        # ... other types

        return Decimal("0")
