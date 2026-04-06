from typing import Any

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    message: str
    data: Any | None = None


class ErrorResponse(BaseModel):
    error: str
    message: str
    detail: Any | None = None
