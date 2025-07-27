from pydantic import BaseModel, Field
from pydantic.types import PositiveInt, NonNegativeInt
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
from app.promotions.domain.promotion import (
    PromotionId,
    PromotionType,
    Promotion,
    PromotionRule,
)
from app.products.domain.entities.product import Product
from app.shared.pagination import PaginationMetadata


class PromotionResponse(BaseModel):
    """
    Pydantic model for representing a Promotion in API responses.
    This mirrors the domain entity's structure, including system-generated fields.
    """

    id: PromotionId = Field(..., description="Unique identifier of the promotion")
    name: str = Field(..., description="Descriptive name of the promotion")
    promotion_type: PromotionType = Field(..., description="Type of promotion")
    discount_value: Decimal = Field(..., description="The value of the discount")

    rule: PromotionRule = Field(
        ..., description="Additional rules for applying the promotion"
    )
    start_date: datetime = Field(
        ..., description="Start date of the promotion's validity"
    )
    end_date: datetime = Field(..., description="End date of the promotion's validity")
    description: Optional[str] = Field(
        None, description="Optional description of the promotion"
    )
    is_active: bool = Field(..., description="Indicates if the promotion is active")
    max_uses: Optional[PositiveInt] = Field(
        None, description="Maximum number of allowed uses (None for unlimited)"
    )
    current_uses: NonNegativeInt = Field(
        ..., description="Current number of times the promotion has been used"
    )
    created_at: datetime = Field(
        ..., description="Timestamp when the promotion was created"
    )
    updated_at: datetime = Field(
        ..., description="Timestamp when the promotion was last updated"
    )
    products: Optional[List[Product]] = Field(
        None, description="List of products applicable to this promotion"
    )

    @classmethod
    def from_domain(
        cls, promotion: Promotion, products: Optional[List[Product]] = None
    ):
        """
        Convert a domain Promotion entity to a PromotionResponse model.
        Optionally include products if provided.
        """
        response = cls(
            id=promotion.id,
            name=promotion.name,
            promotion_type=promotion.promotion_type,
            discount_value=promotion.discount_value,
            rule=promotion.rule,
            start_date=promotion.start_date,
            end_date=promotion.end_date,
            description=promotion.description,
            is_active=promotion.is_active,
            max_uses=promotion.max_uses,
            current_uses=promotion.current_uses,
            created_at=promotion.created_at,
            updated_at=promotion.updated_at,
            products=products,
        )
        return response

    class Config:
        json_encoders = {Decimal: str}
        from_attributes = True


class PromotionSearchResponse(BaseModel):
    """
    Pydantic model for representing a list of promotions in API responses.
    This is used when returning multiple promotions from search queries.
    """

    promotions: List[PromotionResponse] = Field(
        ..., description="List of promotions matching the search criteria"
    )

    paginationMetadata: PaginationMetadata = Field(
        ..., description="Metadata for pagination"
    )

    class Config:
        json_encoders = {Decimal: str}
        from_attributes = True

    @classmethod
    def from_domain(
        cls, promotions: List[Promotion], pagination_metadata: PaginationMetadata
    ):
        """
        Convert a list of domain Promotion entities to a PromotionSearchResponse model.
        """
        if not promotions:
            return cls(promotions=[], paginationMetadata=pagination_metadata)

        promotion_responses = [
            PromotionResponse.from_domain(promotion) for promotion in promotions
        ]
        return cls(
            promotions=promotion_responses,
            paginationMetadata=pagination_metadata,
        )
