from decimal import Decimal
import json
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

        return Promotion(
            id=PromotionId(data.id),
            name=data.name,
            description=data.description,
            promotion_type=PromotionType(data.promotion_type),
            rule=data.rule,
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
        return PromotionModel(
            id=promotion.id.value,
            name=promotion.name,
            description=promotion.description,
            promotion_type=str(promotion.promotion_type.value),
            rule=promotion.rule.to_dict(),
            start_date=promotion.start_date,
            end_date=promotion.end_date,
            is_active=promotion.is_active,
            max_uses=promotion.max_uses,
            current_uses=promotion.current_uses,
            created_at=promotion.created_at,
            updated_at=promotion.updated_at,
        )
