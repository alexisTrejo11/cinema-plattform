from typing import Optional
from pydantic import BaseModel, Field
from app.shared.schema import FoodProductBase, FoodCategoryBase
from uuid import UUID


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


class CreateProductRequest(FoodProductBase):
    """Schema for creating new food products"""

    pass


class InsertProductCategoryRequest(FoodCategoryBase):
    """Schema for creating new food categories"""

    pass
