from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, PositiveInt, NonNegativeInt
from app.promotions.domain.promotion import (
    PromotionId,
    PromotionType,
    Promotion,
)
from app.products.domain.entities.value_objects import ProductId
from app.promotions.domain.promotion_rule_factory import PromotionRule
from app.shared.schema import PydanticUUID


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
    discount_value: Decimal = Field(
        ...,
        gt=0,
        description="The value of the discount (e.g., 10 for 10%, 5.00 for $5)",
    )
    applicable_product_ids: Optional[List[ProductId]] = Field(
        default_factory=list,
        description="List of product IDs to which the promotion applies",
    )
    applicable_category_id: int = Field(
        ...,
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

    def map_to_domain_and_validate_data(self) -> Promotion:
        """
        Converts the Pydantic model to a domain command object.
        """
        promotion = Promotion(
            name=self.name,
            promotion_type=self.promotion_type,
            applicable_product_ids=(
                self.applicable_product_ids if self.applicable_product_ids else []
            ),
            rule=PromotionRule.from_dict(**self.rule),
            start_date=self.start_date,
            end_date=self.end_date,
            description=self.description,
            is_active=self.is_active,
            max_uses=self.max_uses,
        )
        promotion.validate_creation_fields()
        return promotion


class ExtendPromotionCommand(BaseModel):
    """
    Pydantic model for extending an existing Promotion's validity.
    Used as input for an 'extend promotion' use case.
    """

    id: PydanticUUID
    available_until: datetime
