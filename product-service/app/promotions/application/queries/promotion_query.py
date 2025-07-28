from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.promotions.domain.promotion import (
    PromotionId,
    PromotionType,
    ProductId,
)
from app.shared.pagination import PaginationQuery
from pydantic import BaseModel, Field


class GetPromotionByIdQuery(BaseModel):
    """
    Pydantic BaseModel for querying a promotion by its ID.
    """

    id: PromotionId = Field(..., description="The unique ID of the promotion.")
    include_products: bool = Field(
        False, description="Whether to include associated product details."
    )
    pagination: Optional[PaginationQuery] = Field(
        None, description="Pagination details for related products if included."
    )


class GetPromotionByProductIdQuery(BaseModel):
    """
    Pydantic BaseModel for querying promotions by a product ID.
    """

    product_id: ProductId = Field(
        ..., description="The ID of the product to filter promotions by."
    )
    pagination: PaginationQuery = Field(
        ..., description="Pagination information for the query results."
    )
    include_products: bool = Field(
        default=False, description="Whether to include associated product details."
    )


class PromotionQuery(BaseModel):
    """
    Pydantic BaseModel for querying / searching Promotions.
    All fields are optional, allowing flexible filtering.
    Used as input for a 'search promotions' use case.
    """

    id: Optional[PromotionId] = Field(None, description="Filter by unique promotion ID")
    name: Optional[str] = Field(
        None, description="Filter by promotion name (can be partial match)"
    )
    promotion_type: Optional[PromotionType] = Field(
        None, description="Filter by type of promotion"
    )
    is_active: Optional[bool] = Field(None, description="Filter by active status")
    product_id: Optional[ProductId] = Field(
        None, description="Filter promotions applicable to a specific product ID"
    )
    start_date_before: Optional[datetime] = Field(
        None,
        description="Filter promotions starting before this date",
    )
    start_date_after: Optional[datetime] = Field(
        None,
        description="Filter promotions starting after this date",
    )
    end_date_before: Optional[datetime] = Field(
        None,
        description="Filter promotions ending before this date",
    )
    end_date_after: Optional[datetime] = Field(
        None,
        description="Filter promotions ending after this date",
    )
    min_discount_value: Optional[Decimal] = Field(
        None,
        description="Filter by minimum discount value",
        gt=0,  # Pydantic's Field allows validation parameters directly
    )
    max_discount_value: Optional[Decimal] = Field(
        None,
        description="Filter by maximum discount value",
        gt=0,  # Pydantic's Field allows validation parameters directly
    )
    max_uses_reached: Optional[bool] = Field(
        None,
        description="Filter by whether max uses have been reached",
    )
    pagination: Optional[PaginationQuery] = Field(
        None,
        description="Pagination information for the query results",
    )
