from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from decimal import Decimal
from app.products.domain.entities.value_objects import ProductId


class SearchProductsQuery(BaseModel):
    """Parameters for searching food products"""

    offset: int = Field(
        ..., ge=0, description="Pagination offset", json_schema_extra={"example": 0}
    )

    limit: int = Field(
        ...,
        ge=1,
        le=100,
        description="Maximum number of results to return (1-100)",
        json_schema_extra={"example": 10},
    )

    min_price: Optional[Decimal] = Field(
        None, description="Minimum price filter", json_schema_extra={"example": 5.00}
    )

    max_price: Optional[Decimal] = Field(
        None, description="Maximum price filter", json_schema_extra={"example": 20.00}
    )

    name: Optional[str] = Field(
        None,
        description="Name filter (partial match)",
        json_schema_extra={"example": "pizza"},
    )

    category: Optional[int] = Field(
        None, description="Category ID filter", json_schema_extra={"example": 1}
    )

    active_only: bool = Field(
        True,
        description="Whether to include only active products",
        json_schema_extra={"example": True},
    )
    model_config = ConfigDict(arbitrary_types_allowed=True)


class GetProductByIdQuery(BaseModel):
    """Query to get a product by its ID"""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    product_id: ProductId
