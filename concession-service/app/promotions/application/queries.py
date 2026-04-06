import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.shared.pagination import PaginationQuery
from app.promotions.domain.entities.promotion import (
    PromotionId,
    PromotionType,
    ProductId,
)


@dataclass
class GetPromotionByIdQuery:
    """
    Dataclass for querying a promotion by its ID.
    """

    id: PromotionId
    include_products: bool = False
    pagination: Optional[PaginationQuery] = None


@dataclass
class GetPromotionByProductIdQuery:
    """
    Dataclass for querying promotions by a product ID.
    """

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

    id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    promotion_type: Optional[PromotionType] = None
    is_active: Optional[bool] = None
    product_id: Optional[ProductId] = None
    start_date_before: Optional[datetime] = None
    start_date_after: Optional[datetime] = None
    end_date_before: Optional[datetime] = None
    end_date_after: Optional[datetime] = None
    min_discount_value: Optional[Decimal] = None
    max_discount_value: Optional[Decimal] = None
    max_uses_reached: Optional[bool] = None
    pagination: Optional[PaginationQuery] = None
