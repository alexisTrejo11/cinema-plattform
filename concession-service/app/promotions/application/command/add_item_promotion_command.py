from dataclasses import dataclass
from app.products.domain.entities.value_objects import ProductId
from app.promotions.domain.entities.value_objects import PromotionId
from typing import List


@dataclass(frozen=True)
class AddProductsPromotionCommand:
    product_ids: List[ProductId]
    promotion_id: PromotionId


@dataclass(frozen=True)
class RemoveProductsPromotionCommand:
    product_ids: List[ProductId]
    promotion_id: PromotionId


@dataclass(frozen=True)
class AddCategoryPromotionCommand:
    category_id: int
    promotion_id: PromotionId


@dataclass(frozen=True)
class RemoveCategoryPromotionCommand:
    category_id: int
    promotion_id: PromotionId
