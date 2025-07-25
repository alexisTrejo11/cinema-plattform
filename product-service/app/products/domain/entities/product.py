from typing import Optional
from decimal import Decimal
from typing import Optional
from datetime import datetime
from ..validator import ProductValidator
from .value_objects import ProductId
from ..json_mapper import ProductJsonMapper


class Product:
    """Represents a food product in the domain with business validations."""

    def __init__(
        self,
        id: ProductId,
        name: str = "",
        price: Decimal = Decimal("0.00"),
        category_id: int = 0,
        description: Optional[str] = None,
        image_url: Optional[str] = None,
        is_available: bool = True,
        preparation_time_mins: Optional[int] = None,
        calories: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        """
        Initialize a FoodProduct with validation of all attributes.

        Args:
            id: Unique identifier (0 for new products)
            name: Product name (1-200 chars, not just whitespace)
            price: Product price (positive, max 2 decimal places)
            category_id: ID of the category this belongs to
            description: Optional description
            image_url: Optional image URL
            is_available: Availability status
            preparation_time_mins: Optional prep time in minutes (0-240)
            calories: Optional calorie count (0-5000)

        Raises:
            ValueError: For any invalid attribute values
        """
        self.id = id if id else ProductId.generate()
        self.name = name
        self.description = description
        self.price = price
        self.image_url = image_url
        self.is_available = is_available
        self.preparation_time_mins = preparation_time_mins
        self.calories = calories
        self.category_id = category_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

        self.validate()

    def validate(self):
        """Validate all business rules for this product."""
        ProductValidator.validate_product(self)

    def to_dict(self) -> dict:
        """Convert the product to a dictionary representation."""
        return ProductJsonMapper.to_dict(self)

    def to_json(self) -> dict:
        """Convert the product to a JSON string."""
        return ProductJsonMapper.to_json(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        """Create a Product instance from a dictionary."""
        return ProductJsonMapper.from_json(data)

    @classmethod
    def from_json(cls, json_data: dict) -> "Product":
        """Create a Product instance from a JSON string."""
        return ProductJsonMapper.from_json(json_data)

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, price={self.price}, is_available={self.is_available})"

    def __eq__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return (
            self.id == other.id
            and self.name == other.name
            and self.price == other.price
        )

    def __hash__(self):
        return hash((self.id, self.name, self.price))
