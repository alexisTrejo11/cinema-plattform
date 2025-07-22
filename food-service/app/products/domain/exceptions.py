from typing import Any, Dict
from app.shared.base_exceptions import (
    ApplicationException,
    NotFoundException,
    ValidationException,
)


class CategoryNotFoundError(NotFoundException):
    pass


class InvalidCategoryError(ValidationException):
    pass


class ProductNotFoundError(NotFoundException):
    pass


class CategoryNameConflict(ApplicationException):
    def __init__(
        self,
        message: str = "Category Name Conflict",
        error_code: str | None = "CATEGORY_NAME_CONFLICT",
        details: Dict[str, Any] | None = None,
    ):
        super().__init__(message, error_code, details)

    status_code = 409
