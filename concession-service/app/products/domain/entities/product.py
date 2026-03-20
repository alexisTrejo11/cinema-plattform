from typing import Any, Dict, Optional, TYPE_CHECKING
from decimal import Decimal
from typing import Optional
from datetime import datetime
from uuid import UUID
from .value_objects import ProductId
from ..validator import ProductValidator


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

    def validate_product(self):
        """Validate all business rules for this product."""
        ProductValidator.validate_product(self)

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

    def to_dict(self) -> Dict[str, Any]:
        """Converts the FoodProduct instance to a dictionary."""
        return {
            "id": self.id.value if isinstance(self.id, ProductId) else str(self.id),
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "image_url": self.image_url,
            "is_available": self.is_available,
            "preparation_time_mins": self.preparation_time_mins,
            "calories": self.calories,
            "category_id": self.category_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Product":
        """Creates a FoodProduct instance from a dictionary."""
        product_id = data.get("id")
        if isinstance(product_id, str):
            product_id = ProductId.from_string(product_id)
        elif not isinstance(product_id, ProductId):
            product_id = product_id
        elif isinstance(product_id, UUID):
            product_id = ProductId(product_id)

        price = data.get("price", Decimal("0.00"))
        if isinstance(price, str):
            price = Decimal(price)
        elif isinstance(price, float):
            price = Decimal(str(price))
        elif not isinstance(price, Decimal):
            price = Decimal(price)

        created_at = data.get("created_at", datetime.now())
        updated_at = data.get("updated_at", datetime.now())
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)

        return Product(
            id=product_id,
            name=data["name"],
            description=data.get("description"),
            price=price,
            image_url=data.get("image_url"),
            is_available=data["is_available"],
            preparation_time_mins=data.get("preparation_time_mins"),
            calories=data.get("calories"),
            category_id=data["category_id"],
            created_at=created_at,
            updated_at=updated_at,
        )
