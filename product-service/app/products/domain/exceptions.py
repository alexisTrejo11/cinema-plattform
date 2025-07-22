from typing import Any, Dict
from app.shared.base_exceptions import (
    ApplicationException,
    NotFoundException,
    ValidationException,
    DomainException,
)
from typing import Any, Dict, Optional
from http import HTTPStatus


class CategoryNotFoundError(NotFoundException):
    """
    Exception raised when a specific product category cannot be found.
    Inherits from NotFoundException, setting entity_name to "Category".
    """

    def __init__(self, category_id: Any):
        super().__init__(entity_name="Category", entity_id=category_id)


class ProductNotFoundError(NotFoundException):
    """
    Exception raised when a specific product cannot be found.
    Inherits from NotFoundException, setting entity_name to "Product".
    """

    def __init__(self, product_id: Any):
        super().__init__(entity_name="Product", entity_id=product_id)


class InvalidCategoryError(ValidationException):
    """
    Exception raised when a category's data fails specific validation rules.
    Inherits from ValidationException.
    """

    def __init__(
        self,
        field: Optional[str] = None,
        reason: str = "Invalid category data provided.",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(field=field, reason=reason, details=details)
        self.error_code = "INVALID_CATEGORY_DATA"  # More specific error code


class CategoryNameConflict(DomainException):
    """
    Exception raised when an attempt is made to create a category with a name
    that already exists, violating a unique name constraint.
    Maps to HTTP 409 Conflict.
    """

    status_code: int = HTTPStatus.CONFLICT

    def __init__(
        self,
        message: str = "A category with this name already exists.",
        category_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Initializes a CategoryNameConflict exception.

        Args:
            message (str): A human-readable message.
                           Defaults to "A category with this name already exists.".
            category_name (Optional[str]): The conflicting category name.
                                           Defaults to None.
            details (Optional[Dict[str, Any]]): Additional context about the conflict.
                                               Defaults to None.
        """
        _details = {"conflicting_name": category_name}
        if details:
            _details.update(details)
        super().__init__(
            message=message,
            error_code="CATEGORY_NAME_CONFLICT",
            details=_details,
        )
