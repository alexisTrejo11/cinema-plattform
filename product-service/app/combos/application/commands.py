from typing import List
from pydantic import Field
from app.shared.schema import ComboBase, ComboItemBase


class ComboCreateComand(ComboBase):
    """Schema for creating a new combo meal"""

    items: List["ComboItemCreateCommand"] = Field(
        ...,
        description="List of items included in the combo (1-10 items)",
        json_schema_extra={"example": [{"product_id": 1, "quantity": 2}]},
    )


class ComboItemCreateCommand(ComboItemBase):
    """Schema for creating combo items"""

    pass
