from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.combos.domain.combo import ComboBase, ComboItemBase


class ComboCreate(ComboBase):
    items: List['ComboItemCreate']


class ComboUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    discount_percentage: Optional[float] = Field(None, ge=0, le=100)
    image_url: Optional[str] = None
    is_available: Optional[bool] = None
    


class ComboItemCreate(ComboItemBase):
    pass


class ComboItemResponse(ComboItemBase):
    id: int
    product: FoodProductResponse
    
    class Config:
        from_attributes = True