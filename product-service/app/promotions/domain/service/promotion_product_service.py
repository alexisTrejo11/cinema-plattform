from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from ..valueobjects import PromotionId, PromotionType, PromotionRule, ProductId
from app.shared.base_exceptions import DomainException
from ..promotion import Promotion
from app.products.domain.entities.product import Product


class PromotionProductService:
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
    def calculate_product_discount(
        cls, promotion: Promotion, product: Product
    ) -> Decimal:

        if promotion.promotion_type == PromotionType.PERCENTAGE_DISCOUNT:
            return product.price * (promotion.discount_value / Decimal("100"))
        elif promotion.promotion_type == PromotionType.FIXED_DISCOUNT:
            return min(promotion.discount_value, product.price)
        # ... other types

        return Decimal("0")
