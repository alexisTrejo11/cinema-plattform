from typing import List, Optional
from pydantic import BaseModel, Field
from app.combos.domain.entities.value_objects import ComboId
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


class ComboCommandResult(BaseModel):
    """
    Represents the result of a Combo command operation,
    transformed into a Pydantic v2 BaseModel.
    """

    combo_id: str = ""  # Default to empty string for consistency with class methods
    is_success: bool
    message: str = "Combo successfully processed"

    @classmethod
    def error(
        cls, Combo_id: Optional[ComboId] = None, message: str = "error"
    ) -> "ComboCommandResult":
        """
        Returns a new instance with an error message.
        This is a class method to create an error result.
        """
        return cls(
            combo_id=Combo_id.to_string() if Combo_id else "",
            is_success=False,
            message=message,
        )

    @classmethod
    def success(
        cls, combo_id: ComboId, message: str = "success"
    ) -> "ComboCommandResult":
        """
        Returns a new instance with a success message.
        This is a class method to create a success result.
        """
        return cls(combo_id=str(combo_id), is_success=True, message=message)


ComboCreateCommand.model_rebuild()
ComboItemCreateCommand.model_rebuild()
