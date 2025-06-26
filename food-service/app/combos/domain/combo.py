from pydantic import BaseModel, Field
from typing import Optional


class ComboBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    discount_percentage: float = Field(default=0, ge=0, le=100)
    image_url: Optional[str] = None
    is_available: bool = True


class ComboItemBase(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)



class FoodCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_active: bool = True


class FoodCategoryCreate(FoodCategoryBase):
    pass