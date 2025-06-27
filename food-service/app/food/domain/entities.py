from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

class FoodProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    image_url: Optional[str] = None
    is_available: bool = True
    preparation_time_mins: Optional[int] = Field(None, ge=0)
    calories: Optional[int] = Field(None, ge=0)
    category_id: int


class FoodCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_active: bool = True

    def soft_delete(self):
        self.is_active = False
    
class FoodProduct(FoodProductBase):
    id: int = Field(0) #Default
    
    @field_validator('name')
    @classmethod
    def validate_name_not_empty_or_whitespace(cls, v: str) -> str:
        """
        Validates that the name is not just empty or whitespace.
        This adds additional business logic beyond just min_length.
        """
        if not v.strip():
            raise ValueError("Name cannot be empty or contain only whitespace.")
        return v

    @field_validator('price')
    @classmethod
    def validate_price_precision(cls, v: float) -> float:
        """
        Validates that the price has at most two decimal places.
        This is a common business rule for currency.
        """
        if round(v, 2) != v:
            raise ValueError("Price must have at most two decimal places.")
        return v

    @field_validator('preparation_time_mins')
    @classmethod
    def validate_preparation_time_limit(cls, v: Optional[int]) -> Optional[int]:
        """
        Ensures preparation time is within a reasonable business limit (e.g., max 240 minutes).
        Assumes 'ge=0' is already handled by Field, but adds an upper bound.
        """
        if v is not None and v > 240:
            raise ValueError("Preparation time cannot exceed 240 minutes.")
        return v

    @field_validator('calories')
    @classmethod
    def validate_calories_limit(cls, v: Optional[int]) -> Optional[int]:
        """
        Ensures calorie count is within a reasonable business limit (e.g., max 5000 calories).
        Assumes 'ge=0' is already handled by Field, but adds an upper bound.
        """
        if v is not None and v > 5000:
            raise ValueError("Calorie count cannot exceed 5000.")
        return v

    @field_validator('image_url')
    @classmethod
    def validate_image_url_format(cls, v: Optional[str]) -> Optional[str]:
        """
        Basic validation for image URL format.
        This could be expanded with more robust URL validation if needed.
        """
        if v is not None and not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError("Image URL must be a valid HTTP/HTTPS URL.")
        return v


class FoodCategory(FoodCategoryBase):
    id: int = Field(0) #Default


