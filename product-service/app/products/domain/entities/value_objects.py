from uuid import UUID
import uuid
from typing import Any
from app.shared.schema import AbstractId
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


class ProductId(AbstractId):
    """Value object for product ID."""

    def to_string(self) -> str:
        return str(self.value)

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    def from_string(value: str) -> "ProductId":
        """Create a ProductId from a string."""
        try:
            return ProductId(UUID(value))
        except ValueError:
            raise ValueError("Invalid UUID string format")

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

    @classmethod
    def _validate(cls, value: Any) -> "ProductId":
        """Validate input and convert to ProductId."""
        if isinstance(value, cls):
            return value
        elif isinstance(value, str):
            return cls.from_string(value)
        elif isinstance(value, UUID):
            return cls(value)
        else:
            raise ValueError(f"Cannot convert {type(value)} to ProductId")


class ComboId(AbstractId):
    """Value object for combo meal ID."""

    pass
