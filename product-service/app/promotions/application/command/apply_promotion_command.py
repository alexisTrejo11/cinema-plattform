from typing import List
from pydantic import BaseModel
from app.promotions.domain.valueobjects import PromotionId, ProductId


class ApplyPromotionCommand(BaseModel):
    promotion_id: PromotionId
    product_ids: List[ProductId]
