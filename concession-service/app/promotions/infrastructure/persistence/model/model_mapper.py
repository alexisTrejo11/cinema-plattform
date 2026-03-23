from sqlalchemy import inspect

from app.products.domain.entities.value_objects import ProductId
from app.promotions.domain.entities.promotion import Promotion
from app.promotions.domain.entities.value_objects import PromotionId, PromotionType

from .promotion_model import PromotionModel


def promotion_model_to_domain(data: PromotionModel) -> Promotion:
    """Converts the persistence model to a domain entity."""
    state = inspect(data)
    if "products" in state.unloaded or "categories" in state.unloaded:
        applicable_product_ids = []
        applicable_categories_ids = []
    else:
        applicable_product_ids = [
            ProductId(value=product.id) for product in data.products
        ]
        applicable_categories_ids = [category.id for category in data.categories]

    return Promotion(
        id=PromotionId(value=data.id),
        name=data.name,
        description=data.description,
        promotion_type=PromotionType(data.promotion_type),
        rule=data.rule or {},
        start_date=data.start_date,
        end_date=data.end_date,
        is_active=data.is_active,
        max_uses=data.max_uses,
        current_uses=data.current_uses,
        created_at=data.created_at,
        updated_at=data.updated_at,
        applicable_categories_ids=applicable_categories_ids,
        applicable_product_ids=applicable_product_ids,
    )


def promotion_model_from_domain(promotion: Promotion) -> PromotionModel:
    """Creates a persistence model instance from a domain entity."""
    return PromotionModel(
        id=promotion.id.value,
        name=promotion.name,
        description=promotion.description,
        promotion_type=str(promotion.promotion_type.value),
        rule=promotion.rule,
        start_date=promotion.start_date,
        end_date=promotion.end_date,
        is_active=promotion.is_active,
        max_uses=promotion.max_uses,
        current_uses=promotion.current_uses,
        created_at=promotion.created_at,
        updated_at=promotion.updated_at,
    )
