from typing import Optional, Dict, Any


class ProductCategory:
    """Represents a category for food products."""

    def __init__(
        self,
        id: int = 0,
        name: str = "",
        description: Optional[str] = None,
        is_active: bool = True,
    ):
        """
        Initialize a FoodCategory with validation.

        Args:
            id: Unique identifier (0 for new categories)
            name: Category name (1-100 chars)
            description: Optional description
            is_active: Active status

        Raises:
            ValueError: For invalid name
        """
        self.id = id
        self.name = name
        self.description = description
        self.is_active = is_active

        self.validate()

    def validate(self):
        """Validate category attributes."""
        self._validate_name()

    def _validate_name(self):
        """Validate name meets requirements."""
        if not isinstance(self.name, str):
            raise ValueError("Name must be a string")
        if not 1 <= len(self.name) <= 100:
            raise ValueError("Name must be between 1 and 100 characters")

    def soft_delete(self):
        """Mark the category as inactive (soft delete)."""
        self.is_active = False

    def to_dict(self) -> Dict[str, Any]:
        """Converts the FoodCategory instance to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
        }
