from uuid import UUID
import uuid
from typing import Any
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from app.shared.schema import AbstractId


class ComboId(AbstractId):
    @staticmethod
    def generate() -> "ComboId":
        """Generate a new UUID."""
        return ComboId(uuid.uuid4())

    @staticmethod
    def from_string(value: str) -> "ComboId":
        """Create a ComboId from a string."""
        try:
            return ComboId(uuid.UUID(value))
        except ValueError:
            raise ValueError("Invalid UUID string format")


class ComboItemId(AbstractId):
    @staticmethod
    def generate() -> "ComboItemId":
        """Generate a new UUID."""
        return ComboItemId(uuid.uuid4())

    @staticmethod
    def from_string(value: str) -> "ComboItemId":
        """Create a ComboItemId from a string."""
        try:
            return ComboItemId(uuid.UUID(value))
        except ValueError:
            raise ValueError("Invalid UUID string format")
