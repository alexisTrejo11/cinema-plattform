from app.food.domain.entities import FoodProductBase, FoodCategoryBase
from datetime import datetime
from pydantic import BaseModel,Field
from typing import Optional
from dataclasses import dataclass
from decimal import Decimal

class FoodProductCreate(FoodProductBase):
    pass


class FoodProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    image_url: Optional[str] = None
    is_available: Optional[bool] = None
    preparation_time: Optional[int] = Field(None, ge=0)
    calories: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = None


class FoodProductResponse(FoodProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: 'FoodCategoryResponse'
    
    class Config:
        from_attributes = True


class FoodCategoryResponse(FoodCategoryBase):
    id: int
    
    class Config:
        from_attributes = True
        

class FoodCategoryInsert(FoodCategoryBase):
    pass

@dataclass
class SearchFoodParams:
    offset: int
    limit: int
    min_price: Decimal
    max_price: Decimal
    name: str
    category: int 
    active_only: bool
    
    