from typing import Any, Optional, TypeVar, Generic
from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorResponse(BaseModel):
    code: Optional[str] = Field(
        None, description="An optional, machine-readable error code"
    )
    type: Optional[str] = Field(
        None, description="An optional, human-readable type or category of the error"
    )
    message: Optional[str] = Field(
        None, description="A human-readable message describing the error"
    )
    details: Optional[Any] = Field(
        None, description="Additional details about the error, e.g., validation errors"
    )  # Agregamos 'details' para ser consistente

    class Config:
        json_schema_extra = {
            "example": {
                "code": "VALIDATION_ERROR",
                "type": "InputError",
                "message": "The provided email address is invalid.",
            }
        }
