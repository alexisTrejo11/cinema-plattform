from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, PositiveInt
from app.promotions.domain.entities.valueobjects import PromotionType


class PromotionCreateRequest(BaseModel):
    """
    Pydantic model for creating a new Promotion.
    Used as input for a 'create promotion' use case.
    """

    name: str = Field(
        ...,
        min_length=5,
        max_length=100,
        description="Descriptive name of the promotion",
    )

    promotion_type: PromotionType = Field(
        ..., description="Type of promotion (e.g., PERCENTAGE_DISCOUNT, FIXED_DISCOUNT)"
    )

    applicable_product_ids: Optional[List[UUID]] = Field(
        None,
        description="List of product IDs to which the promotion applies",
    )

    applicable_category_id: Optional[int] = Field(
        None,
        description="ID of the category to which the promotion initially applies",
    )
    rule: "PromotionRuleRequest" = Field(
        ..., description="Additional rules for applying the promotion"
    )

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

    class PromotionRuleRequest(BaseModel):
        """
        Pydantic model for the promotion rule.
        Used as part of the PromotionCreateRequest.
        """

        min_quantity: Optional[int] = Field(
            None,
            ge=1,
            le=20,
            description="Minimum quantity of items required for the promotion",
        )

        max_quantity: Optional[int] = Field(
            None,
            ge=1,
            le=100,
            description="Maximum quantity of items allowed for the promotion",
        )
        min_percentage_discount: Optional[Decimal] = Field(
            None,
            ge=0,
            le=100,
            description="Minimum percentage discount allowed for the promotion",
        )
        max_percentage_discount: Optional[Decimal] = Field(
            None,
            ge=0,
            le=100,
            description="Maximum percentage discount allowed for the promotion",
        )

        model_config = ConfigDict(
            arbitrary_types_allowed=True,
        )


class ExtendPromotionRequest(BaseModel):
    """
    Pydantic model for extending an existing Promotion's validity.
    Used as input for an 'extend promotion' use case.
    """

    id: UUID = Field(..., description="Unique identifier of the promotion to extend")

    available_until: datetime = Field(
        ..., description="New end date for the promotion's validity"
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


class PromotionItemRequest(BaseModel):
    """
    Pydantic model for adding a product to a promotion.
    Used as input for an 'add product to promotion' use case.
    """

    productId: list[UUID] = Field(..., description="ID of the product to add")
    promotionId: UUID = Field(
        ..., description="ID of the promotion to which the product will be added"
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
