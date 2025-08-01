from decimal import Decimal
from app.promotions.domain.promotion import (
    Promotion,
    PromotionId,
    ProductId,
    PromotionType,
)
from app.promotions.domain.promotion import Promotion
from app.promotions.domain.promotion_rule_factory import PromotionRule
from .promotion_model import PromotionModel


class PromotionModelMapper:
    @classmethod
    def to_domain(cls, data: PromotionModel) -> Promotion:
        """Converts the model to a domain entity"""
        # Convert rule dict back to domain objects
        rule_dict = data.rule.copy()

        # Convert float back to Decimal
        if rule_dict.get("min_purchase_amount"):
            rule_dict["min_purchase_amount"] = Decimal(
                str(rule_dict["min_purchase_amount"])
            )

        # Convert string UUIDs back to ProductId objects
        if rule_dict.get("required_products"):
            rule_dict["required_products"] = [
                ProductId.from_string(pid) for pid in rule_dict["required_products"]
            ]

        return Promotion(
            id=PromotionId(data.id),
            name=data.name,
            description=data.description,
            promotion_type=PromotionType(data.promotion_type),
            applicable_product_ids=[ProductId(product.id) for product in data.products],
            applicable_categories_ids=[category.id for category in data.categories],
            rule=PromotionRule.from_dict(**rule_dict),
            start_date=data.start_date,
            end_date=data.end_date,
            is_active=data.is_active,
            max_uses=data.max_uses,
            current_uses=data.current_uses,
            created_at=data.created_at,
            updated_at=data.updated_at,
        )

    @classmethod
    def from_domain(cls, promotion: Promotion) -> "PromotionModel":
        """Creates a model instance from a domain entity"""
        rule_dict = promotion.rule.to_dict()

        return PromotionModel(
            id=promotion.id.value,
            name=promotion.name,
            description=promotion.description,
            promotion_type=str(promotion.promotion_type.value),
            rule=rule_dict,
            start_date=promotion.start_date,
            end_date=promotion.end_date,
            is_active=promotion.is_active,
            max_uses=promotion.max_uses,
            current_uses=promotion.current_uses,
        )
