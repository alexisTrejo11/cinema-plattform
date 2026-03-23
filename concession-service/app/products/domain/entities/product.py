from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .value_objects import ProductId
from ..validator import ProductValidator


class Product(BaseModel):
    """Represents a food product in the domain with business validations."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ProductId = Field(default_factory=ProductId.generate)
    name: str = ""
    price: Decimal = Decimal("0.00")
    category_id: int = 0
    description: Optional[str] = None
    image_url: str
    is_available: bool = True
    preparation_time_mins: Optional[int] = None
    calories: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None

    @field_validator("id", mode="before")
    @classmethod
    def _validate_id_field(cls, value: Any) -> ProductId:
        if value in (None, ""):
            return ProductId.generate()
        if isinstance(value, ProductId):
            return value
        if isinstance(value, UUID):
            return ProductId(value)
        if isinstance(value, str):
            return ProductId.from_string(value)
        raise ValueError(f"Cannot convert {type(value)} to ProductId")

    @classmethod
    def create(cls, data: Dict[str, Any]) -> "Product":
        default_image_url: str = "https://via.placeholder.com/150"

        data["id"] = ProductId.generate()
        data["price"] = Decimal(str(data["price"]))
        data["image_url"] = data["image_url"] or default_image_url
        return cls(**data)

    @field_validator("price", mode="before")
    @classmethod
    def _validate_price_field(cls, value: Any) -> Decimal:
        if isinstance(value, Decimal):
            return value
        if isinstance(value, str):
            return Decimal(value)
        if isinstance(value, float):
            return Decimal(str(value))
        return Decimal(value)

    @model_validator(mode="after")
    def _run_business_validation(self) -> "Product":
        ProductValidator.validate_product(self)
        return self

    def validate_business_rules(self):
        """Validate all business rules for this product."""
        ProductValidator.validate_product(self)

    def restore(self) -> "Product":
        self.deleted_at = None
        return self

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name={self.name}, price={self.price}, category_id={self.category_id})"
