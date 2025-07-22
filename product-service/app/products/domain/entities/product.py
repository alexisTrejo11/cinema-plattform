from typing import Any, Dict, Optional
from decimal import Decimal
from typing import Optional
from .value_objects import ProductId, ComboId


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

        self.validate()

    def validate(self):
        """Validate all business rules for this product."""
        self._validate_name()
        self._validate_price()
        self._validate_preparation_time()
        self._validate_calories()

    def _validate_name(self):
        """Validate name meets business requirements."""
        if not isinstance(self.name, str):
            raise ValueError("Name must be a string")
        if not 1 <= len(self.name) <= 200:
            raise ValueError("Name must be between 1 and 200 characters")
        if not self.name.strip():
            raise ValueError("Name cannot be empty or contain only whitespace")

    def _validate_price(self):
        """Validate price meets business requirements."""
        if not isinstance(self.price, (Decimal, int)):
            raise ValueError("Price must be a number")
        if self.price <= Decimal("0.00"):
            raise ValueError("Price must be greater than 0")
        if self.price > Decimal("10000"):
            raise ValueError("Price must be less than 10,000")

    def _validate_preparation_time(self):
        """Validate preparation time if provided."""
        if self.preparation_time_mins is not None:
            if not isinstance(self.preparation_time_mins, int):
                raise ValueError("Preparation time must be an integer")
            if self.preparation_time_mins < 0:
                raise ValueError("Preparation time cannot be negative")
            if self.preparation_time_mins > 240:
                raise ValueError("Preparation time cannot exceed 240 minutes")

    def _validate_calories(self):
        """Validate calories if provided."""
        if self.calories is not None:
            if not isinstance(self.calories, int):
                raise ValueError("Calories must be an integer")
            if self.calories < 0:
                raise ValueError("Calories cannot be negative")
            if self.calories > 5000:
                raise ValueError("Calorie count cannot exceed 5000")

    def to_dict(self) -> Dict[str, Any]:
        """Converts the FoodProduct instance to a dictionary."""
        return {
            "id": self.id.value,  # Extract UUID value from ProductId
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "image_url": self.image_url,
            "is_available": self.is_available,
            "preparation_time_mins": self.preparation_time_mins,
            "calories": self.calories,
            "category_id": self.category_id,
        }
