from typing import Optional, Dict, Any
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ProductCategory(BaseModel):
    """Represents a category for food products."""

    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None

    def validate(self):
        """Validate category attributes."""
        self._validate_name()

    @field_validator("name")
    @classmethod
    def _validate_name_field(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if not 1 <= len(value) <= 100:
            raise ValueError("Name must be between 1 and 100 characters")
        return value

    def _validate_name(self):
        """Validate name meets requirements."""
        if not isinstance(self.name, str):
            raise ValueError("Name must be a string")
        if not 1 <= len(self.name) <= 100:
            raise ValueError("Name must be between 1 and 100 characters")

    def soft_delete(self):
        """Mark the category as inactive (soft delete)."""
        self.is_active = False
        self.deleted_at = datetime.now()

    def restore(self):
        """Restore the category from deleted."""
        self.is_active = True
        self.deleted_at = None
