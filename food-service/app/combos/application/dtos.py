from typing import List, Optional
from datetime import datetime
from app.products.application.dtos import FoodProductResponse
from pydantic import BaseModel, Field
from decimal import Decimal
from app.combos.domain.combo import Combo, ComboItem

class ComboBase(BaseModel):
    """Base model for combo meals with common attributes"""
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Name of the combo meal",
        json_schema_extra={"example": "Family Feast Bundle"}
    )
    
    description: Optional[str] = Field(
        None,
        description="Detailed description of the combo contents",
        json_schema_extra={"example": "Includes 2 large pizzas, garlic bread, and soda"}
    )
    
    price: Decimal = Field(
        ...,
        gt=Decimal('0'),
        decimal_places=2,
        description="Total price of the combo (must be positive, 2 decimal places)",
        json_schema_extra={"example": 29.99}
    )
    
    discount_percentage: Decimal = Field(
        default=Decimal('0'),
        ge=Decimal('0'),
        le=Decimal('100'),
        decimal_places=2,
        description="Percentage discount applied (0-100)",
        json_schema_extra={"example": 15}
    )
    
    image_url: Optional[str] = Field(
        None,
        description="URL to an image of the combo meal",
        json_schema_extra={"example": "https://example.com/images/family-feast.jpg"}
    )
    
    is_available: bool = Field(
        default=True,
        description="Whether the combo is currently available for order",
        json_schema_extra={"example": True}
    )



class ComboItemBase(BaseModel):
    """Base model for items included in a combo meal"""
    
    product_id: int = Field(
        ...,
        description="ID of the product included in the combo",
        json_schema_extra={"example": 42}
    )
    
    quantity: int = Field(
        default=1,
        ge=1,
        le=10,
        description="Quantity of this product in the combo (1-10)",
        json_schema_extra={"example": 2}
    )



class ComboCreate(ComboBase):
    """Schema for creating a new combo meal"""
    
    items: List['ComboItemCreate'] = Field(
        ...,
        description="List of items included in the combo (1-10 items)",
        json_schema_extra={"example": [{"product_id": 1, "quantity": 2}]}
    )


class ComboResponse(ComboBase):
    """Schema for combo meal responses"""
    
    id: int = Field(
        ...,
        description="Unique identifier for the combo",
        json_schema_extra={"example": 1}
    )
    
    combo_items: List['ComboItemResponse'] = Field(
        [],
        description="Detailed information about items in the combo",
        json_schema_extra={"example": [{"product_id": 1, "quantity": 2}]}
    )
    
    created_at: datetime = Field(
        ...,
        description="Timestamp when the combo was created",
        json_schema_extra={"example": "2023-01-01T12:00:00Z"}
    )
    
    updated_at: datetime = Field(
        ...,
        description="Timestamp when the combo was last updated",
        json_schema_extra={"example": "2023-01-01T12:00:00Z"}
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "description": "Complete combo response with items",
            "examples": [{
                "id": 1,
                "name": "Family Bundle",
                "price": 49.99,
                "items": [{"product_id": 1, "quantity": 2}],
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-01T12:00:00Z"
            }]
        }

    @classmethod
    def from_domain(cls, combo: Combo):
        """Convert domain model to DTO"""
        items = [ComboItemResponse(id=item.id, product_id=item.product.id, quantity=item.quantity) for item in combo.items]
        return cls(combo_items=items, **combo.to_dict())

class ComboItemCreate(ComboItemBase):
    """Schema for creating combo items"""
    pass


class ComboItemResponse(ComboItemBase):
    """Schema for combo item responses with full product details"""
    
    id: int = Field(
        ...,
        description="Unique identifier for the combo item",
        json_schema_extra={"example": 1}
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "description": "Complete combo item response",
            "examples": [{
                "id": 1,
                "product_id": 1,
                "quantity": 2
            }]
        }