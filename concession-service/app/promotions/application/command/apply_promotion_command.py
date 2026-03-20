from typing import List
from pydantic import BaseModel
from app.promotions.domain.entities.value_objects import PromotionId, ProductId


class ApplyPromotionCommand(BaseModel):
    promotion_id: PromotionId
    product_ids: List[ProductId]
