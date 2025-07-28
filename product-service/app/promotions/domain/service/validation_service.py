from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from ..valueobjects import PromotionId, PromotionType, PromotionRule, ProductId
from app.shared.base_exceptions import DomainException


class PromotionValidationService:
    @classmethod
    def validate_fields(
        cls,
        name: str,
        discount_value: Decimal,
        rule: PromotionRule,
        start_date: datetime,
        end_date: datetime,
        max_uses: Optional[int] = None,
        current_uses: int = 0,
    ):
        """Validates the creation of a promotion"""
        cls.validate_name(name)
        cls.validate_discount_value(discount_value)
        cls.validate_promotion_rules(rule)
        cls.validate_dates(start_date, end_date)
        cls.validate_uses(max_uses, current_uses)
        cls.validate_promotion_rules(rule)

    @classmethod
    def validate_name(
        cls,
        name: str,
    ):
        """Domain invariant validations"""
        if not name or len(name) > 100:
            raise DomainException(
                "The promotion name must be between 1 and 100 characters"
            )

    @classmethod
    def validate_discount_value(
        cls,
        discount_value: Decimal,
    ):
        """Validates the discount value based on the promotion type"""
        if discount_value <= Decimal("0"):
            raise DomainException("The discount value must be positive")

        if not (0 < discount_value < 100):
            raise DomainException(
                "For discount promotions, the discount must be between 0 and 100."
            )

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

        if rules.required_products and not isinstance(rules.required_products, list):
            raise DomainException("Required products must be a list")

    @staticmethod
    def validate_dates(
        start_date: datetime,
        end_date: datetime,
    ):
        if start_date >= end_date:
            raise DomainException("The start date must be before the end date")

    @staticmethod
    def validate_uses(
        max_uses: Optional[int],
        current_uses: int,
    ):
        if max_uses is not None and max_uses <= 0:
            raise DomainException("Maximum uses must be positive or None")

        if current_uses < 0:
            raise DomainException("The usage counter cannot be negative")

        if max_uses is not None and current_uses > max_uses:
            raise DomainException("Current uses cannot exceed the maximum allowed")
