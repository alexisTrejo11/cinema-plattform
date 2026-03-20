from uuid import UUID
from app.products.domain.entities.product import Product, ProductId
from ..exceptions import *
from .value_objects import ComboItemId


class ComboItem:
    """Represents an individual food product within a combo.

    Attributes:
        product: The Product included in the combo
        quantity: Quantity of this product in the combo (1-10)
    """

    def __init__(self, product: Product, id: ComboItemId, quantity: int = 1):
        """Initializes a ComboItem with validation.

        Args:
            product: Product to include in combo
            quantity: Quantity of this product (default 1)

        Raises:
            TypeError: If product is not a Product or quantity is not an integer
        """
        if id:
            if not isinstance(id, ComboItemId):
                raise TypeError("id must be an ComboItemId instance")
        if not isinstance(product, Product):
            raise TypeError("product id must be an instance of Product")
        if not isinstance(quantity, int):
            raise TypeError("quantity must be an integer")

        self.id = id if id else ComboItemId.generate()
        self.product = product
        self.quantity = quantity

    def validate_quantity_range(self):
        """Validates that quantity is within allowed range (1-10).

        Raises:
            QuantityRangeException: If quantity is outside 1-10 range
        """
        min_quantity = 1
        max_quantity = 10
        if not (min_quantity <= self.quantity <= max_quantity):
            raise QuantityRangeException(
                self.product.id.to_string(), min_quantity, max_quantity
            )

    def to_dict(self) -> dict:
        """Converts ComboItem to dictionary representation."""
        return {
            "id": self.id.value,
            "product_id": self.product.id.value,
            "quantity": self.quantity,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ComboItem":
        """Creates a ComboItem instance from a dictionary representation."""
        if isinstance(data["id"], str):
            data["id"] = ComboItemId.from_string(data["id"])

        if isinstance(data["id"], UUID):
            data["id"] = ComboItemId(data["product_id"])

        if isinstance(data["product_id"], str):
            data["product_id"] = ProductId.from_string(data["product_id"])

        if isinstance(data["product_id"], UUID):
            data["product_id"] = ProductId(data["product_id"])

        return cls(product=data["product"], id=data["id"], quantity=data["quantity"])

    def to_json(self) -> dict:
        """Converts ComboItem to JSON serializable dictionary."""
        return {
            "id": self.id.to_string(),
            "product": self.product.to_json(),
            "quantity": self.quantity,
        }

    @classmethod
    def from_json(cls, data: dict) -> "ComboItem":
        """Creates a ComboItem instance from a dictionary representation."""
        if isinstance(data["id"], str):
            data["id"] = ComboItemId.from_string(data["id"])

        if isinstance(data["product_id"], str):
            data["product_id"] = ProductId.from_string(data["product_id"])

        return cls(product=data["product"], id=data["id"], quantity=data["quantity"])
