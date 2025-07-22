from uuid import UUID
import uuid
from typing import Any
from app.shared.schema import AbstractId


class ProductId(AbstractId):
    """Value object for product ID."""

    def to_string(self) -> str:
        return str(self.value)

    @staticmethod
    def generate() -> "ProductId":
        """Generate a new ProductId."""
        return ProductId(uuid.uuid4())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ProductId):
            return NotImplemented
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return f"ProductId({self.value})"


class ComboId(AbstractId):
    """Value object for combo meal ID."""

    pass
