from typing import Any, Optional, TYPE_CHECKING
import uuid
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

if TYPE_CHECKING:
    from app.products.domain.entities.value_objects import ProductId


class ComboBase(BaseModel):
    """Base model for combo meals with common attributes"""

    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Name of the combo meal",
        json_schema_extra={"example": "Family Feast Bundle"},
    )

    description: Optional[str] = Field(
        None,
        description="Detailed description of the combo contents",
        json_schema_extra={
            "example": "Includes 2 large pizzas, garlic bread, and soda"
        },
    )

    price: Decimal = Field(
        ...,
        gt=Decimal("0"),
        decimal_places=2,
        description="Total price of the combo (must be positive, 2 decimal places)",
        json_schema_extra={"example": 29.99},
    )

    discount_percentage: Decimal = Field(
        default=Decimal("0"),
        ge=Decimal("0"),
        le=Decimal("100"),
        decimal_places=2,
        description="Percentage discount applied (0-100)",
        json_schema_extra={"example": 15},
    )

    image_url: Optional[str] = Field(
        None,
        description="URL to an image of the combo meal",
        json_schema_extra={"example": "https://example.com/images/family-feast.jpg"},
    )

    is_available: bool = Field(
        default=True,
        description="Whether the combo is currently available for order",
        json_schema_extra={"example": True},
    )


class ComboItemBase(BaseModel):
    """Base model for items included in a combo meal"""

    product_id: "uuid.UUID" = Field(
        ...,
        description="ID of the product included in the combo",
        json_schema_extra={"example": "1234567890-abcdef123456-1234567890abcdef"},
    )

    quantity: int = Field(
        default=1,
        ge=1,
        le=10,
        description="Quantity of this product in the combo (1-10)",
        json_schema_extra={"example": 2},
    )


class ProductBase(BaseModel):
    """Base model for food products with common attributes"""

    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Name of the food product (1-200 characters)",
        json_schema_extra={"example": "Margherita Pizza"},
    )

    description: Optional[str] = Field(
        None,
        description="Optional description of the food product",
        json_schema_extra={"example": "Classic pizza with tomato sauce and mozzarella"},
    )

    price: float = Field(
        ...,
        gt=0,
        description="Price of the product (must be positive)",
        json_schema_extra={"example": 12.99},
    )

    image_url: Optional[str] = Field(
        None,
        description="URL to an image of the product",
        json_schema_extra={"example": "https://example.com/pizza.jpg"},
    )

    is_available: bool = Field(
        True,
        description="Availability status of the product",
        json_schema_extra={"example": True},
    )

    preparation_time_mins: Optional[int] = Field(
        None,
        ge=0,
        description="Estimated preparation time in minutes (optional)",
        json_schema_extra={"example": 20},
    )

    calories: Optional[int] = Field(
        None,
        ge=0,
        description="Calorie count (optional)",
        json_schema_extra={"example": 800},
    )

    category_id: int = Field(
        ...,
        description="ID of the category this product belongs to",
        json_schema_extra={"example": 1},
    )


class ProductCategoryBase(BaseModel):
    """Base model for food categories with common attributes"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the category (1-100 characters)",
        json_schema_extra={"example": "Pizzas"},
    )

    description: Optional[str] = Field(
        None,
        description="Optional description of the category",
        json_schema_extra={"example": "Various types of pizzas"},
    )

    is_active: bool = Field(
        True,
        description="Active status of the category",
        json_schema_extra={"example": True},
    )


class PydanticUUID(BaseModel):
    """
    Base ID class as a Pydantic Model.
    Provides immutability, validation, and auto-serialization.
    """

    value: uuid.UUID = Field(default_factory=uuid.uuid4)

    def __init__(self, value: uuid.UUID):
        super().__init__(value=value)

    def to_string(self) -> str:
        return str(self.value)

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def generate(cls) -> "PydanticUUID":
        """Factory method to create a new ID."""
        return cls.model_construct(value=uuid.uuid4())

    @classmethod
    def from_string(cls, v: str) -> "PydanticUUID":
        """Manual factory for strings."""
        return cls.model_construct(value=uuid.UUID(v))

    @model_validator(mode="before")
    @classmethod
    def _coerce_root_input(cls, data: Any) -> Any:
        if isinstance(data, cls):
            return data
        if isinstance(data, uuid.UUID):
            return {"value": data}
        if isinstance(data, str):
            return {"value": data}
        return data

    @field_validator("value", mode="before")
    @classmethod
    def _coerce_value(cls, v: Any) -> uuid.UUID:
        if isinstance(v, uuid.UUID):
            return v
        if isinstance(v, str):
            return uuid.UUID(v)
        raise ValueError(
            f"Cannot convert {type(v).__name__!r} to UUID for {cls.__name__}"
        )
