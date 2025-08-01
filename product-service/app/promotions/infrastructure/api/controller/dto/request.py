from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, PositiveInt, NonNegativeInt
from app.promotions.domain.promotion import (
    PromotionId,
    PromotionType,
)
from app.promotions.domain.promotion_rule_factory import PromotionRule
from app.products.domain.entities.value_objects import ProductId


class PromotionCreateRequest(BaseModel):
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
    applicable_product_ids: List[UUID] = Field(
        default_factory=list,
        description="List of product IDs to which the promotion applies",
    )
    applicable_category_id: int = Field(
        ...,
        description="ID of the category to which the promotion initialies applies",
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

    class PromotionRuleRequest(BaseModel):
        """
        Pydantic model for defining rules associated with a Promotion.
        """

        required_products: List[UUID] = Field(
            default_factory=list,
            description="List of product IDs that must be included for the promotion to apply",
        )
        min_quantity: Optional[int] = Field(
            None, description="Minimum quantity required for the promotion to apply"
        )
        max_quantity: Optional[int] = Field(
            None, description="Maximum quantity allowed for the promotion"
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


class PromotionUpdateRequest(BaseModel):
    """
    Pydantic model for updating an existing Promotion.
    All fields are optional, allowing partial updates.
    Used as input for an 'update promotion' use case.
    """

    id: PromotionId = Field(
        ..., description="Unique identifier of the promotion to update"
    )
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Descriptive name of the promotion",
    )
    promotion_type: Optional[PromotionType] = Field(
        None,
        description="Type of promotion (e.g., PERCENTAGE_DISCOUNT, FIXED_DISCOUNT)",
    )
    discount_value: Optional[Decimal] = Field(
        None, gt=0, description="The value of the discount"
    )
    applicable_product_ids: Optional[List[ProductId]] = Field(
        None, description="List of product IDs to which the promotion applies"
    )
    rule: Optional[PromotionRule] = Field(
        None, description="Additional rules for applying the promotion"
    )
    start_date: Optional[datetime] = Field(
        None, description="Start date of the promotion's validity"
    )
    end_date: Optional[datetime] = Field(
        None, description="End date of the promotion's validity"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Optional description of the promotion"
    )
    is_active: Optional[bool] = Field(
        None, description="Indicates if the promotion is active"
    )
    max_uses: Optional[PositiveInt] = Field(
        None, description="Maximum number of allowed uses (None for unlimited)"
    )
    current_uses: Optional[NonNegativeInt] = Field(
        None, description="Current number of times the promotion has been used"
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
