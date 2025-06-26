from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class FoodProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    image_url: Optional[str] = None
    is_available: bool = True
    preparation_time: Optional[int] = Field(None, ge=0)
    calories: Optional[int] = Field(None, ge=0)
    category_id: int


class FoodCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_active: bool = True

    def soft_delete(self):
        self.is_active = True
    
class FoodProduct(FoodProductBase):
    pass


class FoodCategory(FoodCategoryBase):
    id: int = Field(0) #Default


