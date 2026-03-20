from app.shared.schema import ComboBase, ComboItemBase
from typing import List
from pydantic import Field


class ComboItemCreateRequest(ComboItemBase):
    """Schema for creating combo items"""

    pass


class ComboCreateRequest(ComboBase):
    """Schema for creating a new combo meal"""

    items: List["ComboItemCreateRequest"] = Field(
        ...,
        description="List of items included in the combo (1-10 items)",
        json_schema_extra={"example": [{"product_id": "prod_123", "quantity": 2}]},
    )


class PaginationQuery:
    """Schema for pagination query parameters"""

    page: int = Field(1, ge=1, description="Page number for pagination")
    size: int = Field(10, ge=1, le=100, description="Number of items per page")
