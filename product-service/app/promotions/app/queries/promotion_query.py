from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic.types import PositiveInt, NonNegativeInt
from app.promotions.domain.promotion import (
    PromotionId,
    PromotionType,
    ProductId,
    PromotionRule,
)
from app.shared.pagination import PaginationQuery
from dataclasses import dataclass, field


@dataclass
class GetPromotionByIdQuery:
    """Data class for querying a promotion by its ID."""

    id: PromotionId
    include_products: bool = False
    page: Optional[PaginationQuery] = None


@dataclass
class GetPromotionByProductIdQuery:
    """Data class for querying a promotion by its ID."""

    product_id: ProductId
    pagination: PaginationQuery
    include_products: bool = False


@dataclass
class PromotionQuery:
    """
    Dataclass for querying / searching Promotions.
    All fields are optional, allowing flexible filtering.
    Used as input for a 'search promotions' use case.
    """

    id: Optional[PromotionId] = field(
        default=None, metadata={"description": "Filter by unique promotion ID"}
    )
    name: Optional[str] = field(
        default=None,
        metadata={"description": "Filter by promotion name (can be partial match)"},
    )
    promotion_type: Optional[PromotionType] = field(
        default=None, metadata={"description": "Filter by type of promotion"}
    )
    is_active: Optional[bool] = field(
        default=None, metadata={"description": "Filter by active status"}
    )
    product_id: Optional[ProductId] = field(
        default=None,
        metadata={
            "description": "Filter promotions applicable to a specific product ID"
        },
    )
    start_date_before: Optional[datetime] = field(
        default=None,
        metadata={"description": "Filter promotions starting before this date"},
    )
    start_date_after: Optional[datetime] = field(
        default=None,
        metadata={"description": "Filter promotions starting after this date"},
    )
    end_date_before: Optional[datetime] = field(
        default=None,
        metadata={"description": "Filter promotions ending before this date"},
    )
    end_date_after: Optional[datetime] = field(
        default=None,
        metadata={"description": "Filter promotions ending after this date"},
    )
    min_discount_value: Optional[Decimal] = field(
        default=None,
        metadata={"description": "Filter by minimum discount value", "gt": 0},
    )
    max_discount_value: Optional[Decimal] = field(
        default=None,
        metadata={"description": "Filter by maximum discount value", "gt": 0},
    )
    max_uses_reached: Optional[bool] = field(
        default=None,
        metadata={"description": "Filter by whether max uses have been reached"},
    )
    pagination: Optional[PaginationQuery] = field(
        default=None,
        metadata={"description": "Pagination information for the query results"},
    )
