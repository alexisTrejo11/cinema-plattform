from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from ..valueobjects import PromotionId, PromotionType, PromotionRule, ProductId
from app.shared.base_exceptions import DomainException


class PromotionValidationService:
    @staticmethod
    def validate_fields(
        name: str,
        discount_value: Decimal,
        start_date: datetime,
        end_date: datetime,
        max_uses: Optional[int],
        current_uses: int,
    ):
        """Domain invariant validations"""
        if not name or len(name) > 100:
            raise DomainException(
                "The promotion name must be between 1 and 100 characters"
            )

        if discount_value <= Decimal("0"):
            raise DomainException("The discount value must be positive")

        if start_date >= end_date:
            raise DomainException("The start date must be before the end date")

        if max_uses is not None and max_uses <= 0:
            raise DomainException("Maximum uses must be positive or None")

        if current_uses < 0:
            raise DomainException("The usage counter cannot be negative")

        if max_uses is not None and current_uses > max_uses:
            raise DomainException("Current uses cannot exceed the maximum allowed")

    @staticmethod
    def validate_promotion_rules(rules: PromotionRule):
        """Validates the promotion rules"""
        if rules.min_quantity is not None and rules.min_quantity <= 0:
            raise DomainException("Minimum quantity must be positive")

        if (
            rules.min_purchase_amount is not None
            and rules.min_purchase_amount <= Decimal("0")
        ):
            raise DomainException("Minimum purchase amount must be positive")

        if rules.applicable_categories and not isinstance(
            rules.applicable_categories, list
        ):
            raise DomainException("Applicable categories must be a list")

        if rules.required_products and not isinstance(rules.required_products, list):
            raise DomainException("Required products must be a list")
