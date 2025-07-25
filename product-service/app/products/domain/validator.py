from decimal import Decimal
from uuid import UUID
from .entities.product import Product


class ProductValidator:
    """Validator for Product entities."""

    @staticmethod
    def validate_product(product: "Product") -> None:
        ProductValidator._validate_name(product)
        ProductValidator._validate_price(product)
        ProductValidator._validate_preparation_time(product)
        ProductValidator._validate_calories(product)
        ProductValidator._validate_id(product)

    @staticmethod
    def _validate_id(product: "Product") -> None:
        """Validate the product ID."""
        if isinstance(product.id.value, UUID):
            raise ValueError("ID must be a valid UUID")

    @staticmethod
    def _validate_name(product: "Product") -> None:
        """Validate name meets business requirements."""
        if not isinstance(product.name, str):
            raise ValueError("Name must be a string")
        if not 1 <= len(product.name) <= 200:
            raise ValueError("Name must be between 1 and 200 characters")
        if not product.name.strip():
            raise ValueError("Name cannot be empty or contain only whitespace")

    @staticmethod
    def _validate_price(product: "Product") -> None:
        """Validate price meets business requirements."""
        if not isinstance(product.price, (Decimal, int)):
            raise ValueError("Price must be a number")
        if product.price <= Decimal("0.00"):
            raise ValueError("Price must be greater than 0")
        if product.price > Decimal("10000"):
            raise ValueError("Price must be less than 10,000")

    @staticmethod
    def _validate_preparation_time(product: "Product") -> None:
        """Validate preparation time if provided."""
        if product.preparation_time_mins is not None:
            if not isinstance(product.preparation_time_mins, int):
                raise ValueError("Preparation time must be an integer")
            if product.preparation_time_mins < 0:
                raise ValueError("Preparation time cannot be negative")
            if product.preparation_time_mins > 240:
                raise ValueError("Preparation time cannot exceed 240 minutes")

    @staticmethod
    def _validate_calories(product: "Product") -> None:
        """Validate calories if provided."""
        if product.calories is not None:
            if not isinstance(product.calories, int):
                raise ValueError("Calories must be an integer")
            if product.calories < 0:
                raise ValueError("Calories cannot be negative")
            if product.calories > 5000:
                raise ValueError("Calories count cannot exceed 5000")
