from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field
from app.shared.schema import ProductCategoryBase, ProductBase
from uuid import UUID
from enum import Enum
from pydantic import ConfigDict


class ProductSortField(str, Enum):
    NAME = "name"
    PRICE = "price"
    CREATED_AT = "created_at"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class ProductSearchQuery(BaseModel):
    offset: int = Field(
        default=0,
        ge=0,
        description="Pagination offset",
        json_schema_extra={"example": 0},
    )
    limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of results to return (1-100)",
        json_schema_extra={"example": 10},
    )
    category_id: Optional[int] = Field(
        default=None,
        ge=1,
        description="Filter by category ID",
        json_schema_extra={"example": 1},
    )
    min_price: Optional[Decimal] = Field(
        default=None,
        description="Minimum price filter",
        json_schema_extra={"example": 5.00},
    )
    max_price: Optional[Decimal] = Field(
        default=None,
        description="Maximum price filter",
        json_schema_extra={"example": 20.00},
    )
    name_like: Optional[str] = Field(
        default=None,
        description="Filter by product name (partial match)",
        json_schema_extra={"example": "pizza"},
    )
    available_only: bool = Field(
        default=True,
        description="Only include available products",
        json_schema_extra={"example": True},
    )
    sort_by: ProductSortField = Field(
        default=ProductSortField.NAME,
        description="Field to sort by",
        json_schema_extra={"example": "name"},
    )
    sort_order: SortOrder = Field(
        default=SortOrder.ASC,
        description="Sort order",
        json_schema_extra={"example": "asc"},
    )

    # Configuración adicional para Pydantic v2
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Parameters for product search and filtering",
            "examples": [
                {
                    "offset": 0,
                    "limit": 10,
                    "category_id": 1,
                    "min_price": 10.50,
                    "max_price": 50.00,
                    "name_like": "pizza",
                    "available_only": True,
                    "sort_by": "price",
                    "sort_order": "desc",
                }
            ],
        }
    )


class UpdateProductRequest(BaseModel):
    product_id: UUID = Field(
        ...,
        description="ID of the product to update",
    )
    """Schema for updating existing food products (all fields optional)"""
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Updated name of the product",
        json_schema_extra={"example": "Updated Pizza Name"},
    )

    description: Optional[str] = Field(
        None,
        description="Updated description",
        json_schema_extra={"example": "Updated description"},
    )

    price: Optional[float] = Field(
        None, gt=0, description="Updated price", json_schema_extra={"example": 14.99}
    )

    image_url: Optional[str] = Field(
        None,
        description="Updated image URL",
        json_schema_extra={"example": "https://example.com/new-pizza.jpg"},
    )

    is_available: Optional[bool] = Field(
        None,
        description="Updated availability status",
        json_schema_extra={"example": False},
    )

    preparation_time: Optional[int] = Field(
        None,
        ge=0,
        description="Updated preparation time",
        json_schema_extra={"example": 25},
    )

    calories: Optional[int] = Field(
        None,
        ge=0,
        description="Updated calorie count",
        json_schema_extra={"example": 850},
    )

    category_id: Optional[int] = Field(
        None, description="Updated category ID", json_schema_extra={"example": 2}
    )


class CreateProductRequest(ProductBase):
    """Schema for creating new food products"""

    pass


class CategoryRequest(ProductCategoryBase):
    """Schema for creating new food categories"""

    pass
