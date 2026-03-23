from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from app.products.domain.entities.value_objects import ProductId
from app.promotions.domain.entities.promotion import (
    Promotion,
    PromotionType,
    PromotionId,
)

_ITEM_CMD_CONFIG = ConfigDict(arbitrary_types_allowed=True, frozen=True)


class AddProductsPromotionCommand(BaseModel):
    product_ids: List[ProductId]
    promotion_id: PromotionId

    model_config = _ITEM_CMD_CONFIG


class RemoveProductsPromotionCommand(BaseModel):
    product_ids: List[ProductId]
    promotion_id: PromotionId

    model_config = _ITEM_CMD_CONFIG


class AddCategoryPromotionCommand(BaseModel):
    category_id: int
    promotion_id: PromotionId

    model_config = _ITEM_CMD_CONFIG


class RemoveCategoryPromotionCommand(BaseModel):
    category_id: int
    promotion_id: PromotionId

    model_config = _ITEM_CMD_CONFIG


class PromotionCreateCommand(BaseModel):
    """
    Pydantic model for creating a new Promotion.
    Used as input for a 'create promotion' use case.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Descriptive name of the promotion",
    )
    promotion_type: PromotionType = Field(
        ..., description="Type of promotion (e.g., PERCENTAGE_DISCOUNT, FIXED_DISCOUNT)"
    )
    applicable_product_ids: Optional[List[ProductId]] = Field(
        default_factory=list,
        description="List of product IDs to which the promotion applies",
    )
    applicable_category_id: Optional[int] = Field(
        None,
        description="ID of the category to which the promotion applies",
    )
    rule: dict = Field(..., description="Additional rules for applying the promotion")
    start_date: datetime = Field(
        ..., description="Start date of the promotion's validity"
    )
    end_date: datetime = Field(..., description="End date of the promotion's validity")
    description: Optional[str] = Field(
        None, max_length=500, description="Optional description of the promotion"
    )
    is_active: bool = Field(True, description="Indicates if the promotion is active")
    max_uses: Optional[PositiveInt] = Field(
        None, description="Maximum number of allowed uses (None for unlimited)"
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    def map_to_domain(self) -> Promotion:
        return Promotion(
            name=self.name,
            promotion_type=self.promotion_type,
            applicable_product_ids=(
                list(self.applicable_product_ids) if self.applicable_product_ids else []
            ),
            rule=self.rule,
            start_date=self.start_date,
            end_date=self.end_date,
            description=self.description,
            is_active=self.is_active,
            max_uses=self.max_uses,
        )


class ExtendPromotionCommand(BaseModel):
    """Pydantic model for extending an existing Promotion's validity."""

    id: PromotionId
    available_until: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ApplyPromotionCommand(BaseModel):
    promotion_id: PromotionId
    product_ids: List[ProductId]
