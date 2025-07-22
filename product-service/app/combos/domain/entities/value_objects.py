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


class ComboItemId(AbstractId):
    @staticmethod
    def generate() -> "ComboItemId":
        """Generate a new UUID."""
        return ComboItemId(uuid.uuid4())
