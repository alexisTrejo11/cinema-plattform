from typing import List
from pydantic import Field
from app.shared.schema import ComboBase, ComboItemBase


class ComboItemCreateCommand(ComboItemBase):
    """Schema for creating combo items"""

    pass


class ComboCreateCommand(ComboBase):
    """Schema for creating a new combo meal"""

    items: List["ComboItemCreateCommand"] = Field(
        ...,
        description="List of items included in the combo (1-10 items)",
        json_schema_extra={"example": [{"product_id": "prod_123", "quantity": 2}]},
    )


ComboCreateCommand.model_rebuild()
ComboItemCreateCommand.model_rebuild()
