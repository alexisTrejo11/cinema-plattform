from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class FoodProductBase(BaseModel):
    """Base model for food products with common attributes"""
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Name of the food product (1-200 characters)",
        json_schema_extra={"example": "Margherita Pizza"}
    )
    
    description: Optional[str] = Field(
        None,
        description="Optional description of the food product",
        json_schema_extra={"example": "Classic pizza with tomato sauce and mozzarella"}
    )
    
    price: float = Field(
        ...,
        gt=0,
        description="Price of the product (must be positive)",
        json_schema_extra={"example": 12.99}
    )
    
    image_url: Optional[str] = Field(
        None,
        description="URL to an image of the product",
        json_schema_extra={"example": "https://example.com/pizza.jpg"}
    )
    
    is_available: bool = Field(
        True,
        description="Availability status of the product",
        json_schema_extra={"example": True}
    )
    
    preparation_time_mins: Optional[int] = Field(
        None,
        ge=0,
        description="Estimated preparation time in minutes (optional)",
        json_schema_extra={"example": 20}
    )
    
    calories: Optional[int] = Field(
        None,
        ge=0,
        description="Calorie count (optional)",
        json_schema_extra={"example": 800}
    )
    
    category_id: int = Field(
        ...,
        description="ID of the category this product belongs to",
        json_schema_extra={"example": 1}
    )


class FoodCategoryBase(BaseModel):
    """Base model for food categories with common attributes"""
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the category (1-100 characters)",
        json_schema_extra={"example": "Pizzas"}
    )
    
    description: Optional[str] = Field(
        None,
        description="Optional description of the category",
        json_schema_extra={"example": "Various types of pizzas"}
    )
    
    is_active: bool = Field(
        True,
        description="Active status of the category",
        json_schema_extra={"example": True}
    )

    def soft_delete(self):
        """Marks the category as inactive (soft delete)"""
        self.is_active = False


class FoodProductCreate(FoodProductBase):
    """Schema for creating new food products"""
    pass


class FoodProductUpdate(BaseModel):
    """Schema for updating existing food products (all fields optional)"""
    
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Updated name of the product",
        json_schema_extra={"example": "Updated Pizza Name"}
    )
    
    description: Optional[str] = Field(
        None,
        description="Updated description",
        json_schema_extra={"example": "Updated description"}
    )
    
    price: Optional[float] = Field(
        None,
        gt=0,
        description="Updated price",
        json_schema_extra={"example": 14.99}
    )
    
    image_url: Optional[str] = Field(
        None,
        description="Updated image URL",
        json_schema_extra={"example": "https://example.com/new-pizza.jpg"}
    )
    
    is_available: Optional[bool] = Field(
        None,
        description="Updated availability status",
        json_schema_extra={"example": False}
    )
    
    preparation_time: Optional[int] = Field(
        None,
        ge=0,
        description="Updated preparation time",
        json_schema_extra={"example": 25}
    )
    
    calories: Optional[int] = Field(
        None,
        ge=0,
        description="Updated calorie count",
        json_schema_extra={"example": 850}
    )
    
    category_id: Optional[int] = Field(
        None,
        description="Updated category ID",
        json_schema_extra={"example": 2}
    )


class FoodProductResponse(FoodProductBase):
    """Response model for food products including ID"""
    
    id: int = Field(
        ...,
        description="Unique identifier of the product",
        json_schema_extra={"example": 1}
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Margherita Pizza",
                "description": "Classic pizza",
                "price": 12.99,
                "image_url": "https://example.com/pizza.jpg",
                "is_available": True,
                "preparation_time_mins": 20,
                "calories": 800,
                "category_id": 1
            }
        }


class FoodCategoryResponse(FoodCategoryBase):
    """Response model for food categories including ID"""
    
    id: int = Field(
        ...,
        description="Unique identifier of the category",
        json_schema_extra={"example": 1}
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Pizzas",
                "description": "Various pizza types",
                "is_active": True
            }
        }


class FoodCategoryInsert(FoodCategoryBase):
    """Schema for inserting new food categories"""
    pass


class SearchFoodParams(BaseModel):
    """Parameters for searching food products"""
    
    offset: int = Field(
        ...,
        ge=0,
        description="Pagination offset",
        json_schema_extra={"example": 0}
    )
    
    limit: int = Field(
        ...,
        ge=1,
        le=100,
        description="Maximum number of results to return (1-100)",
        json_schema_extra={"example": 10}
    )
    
    min_price: Optional[Decimal] = Field(
        None,
        description="Minimum price filter",
        json_schema_extra={"example": 5.00}
    )
    
    max_price: Optional[Decimal] = Field(
        None,
        description="Maximum price filter",
        json_schema_extra={"example": 20.00}
    )
    
    name: Optional[str] = Field(
        None,
        description="Name filter (partial match)",
        json_schema_extra={"example": "pizza"}
    )
    
    category: Optional[int] = Field(
        None,
        description="Category ID filter",
        json_schema_extra={"example": 1}
    )
    
    active_only: bool = Field(
        True,
        description="Whether to include only active products",
        json_schema_extra={"example": True}
    )

    class Config:
        json_schema_extra = {
            "example": {
                "offset": 0,
                "limit": 10,
                "min_price": 5.00,
                "max_price": 20.00,
                "name": "pizza",
                "category": 1,
                "active_only": True
            }
        }