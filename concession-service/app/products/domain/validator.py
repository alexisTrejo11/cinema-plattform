from decimal import Decimal
from uuid import UUID
from typing import TYPE_CHECKING
from app.shared.base_exceptions import ValidationException

if TYPE_CHECKING:
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
        if not isinstance(product.id.value, UUID):
            raise ValidationException("ID must be a valid UUID")

    @staticmethod
    def _validate_name(product: "Product") -> None:
        """Validate name meets business requirements."""
        if not isinstance(product.name, str):
            raise ValidationException("Name must be a string")
        if not 1 <= len(product.name) <= 200:
            raise ValidationException("Name must be between 1 and 200 characters")
        if not product.name.strip():
            raise ValidationException("Name cannot be empty or contain only whitespace")

    @staticmethod
    def _validate_price(product: "Product") -> None:
        """Validate price meets business requirements."""
        if not isinstance(product.price, (Decimal, int)):
            raise ValidationException("Price must be a number")
        if product.price <= Decimal("0.00"):
            raise ValidationException("Price must be greater than 0")
        if product.price > Decimal("10000"):
            raise ValidationException("Price must be less than 10,000")

    @staticmethod
    def _validate_preparation_time(product: "Product") -> None:
        """Validate preparation time if provided."""
        if product.preparation_time_mins is not None:
            if not isinstance(product.preparation_time_mins, int):
                raise ValidationException("Preparation time must be an integer")
            if product.preparation_time_mins < 0:
                raise ValidationException("Preparation time cannot be negative")
            if product.preparation_time_mins > 240:
                raise ValidationException("Preparation time cannot exceed 240 minutes")

    @staticmethod
    def _validate_calories(product: "Product") -> None:
        """Validate calories if provided."""
        if product.calories is not None:
            if not isinstance(product.calories, int):
                raise ValidationException("Calories must be an integer")
            if product.calories < 0:
                raise ValidationException("Calories cannot be negative")
            if product.calories > 5000:
                raise ValidationException("Calories count cannot exceed 5000")
