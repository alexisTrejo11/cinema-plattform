from typing import Any

from fastapi.exceptions import RequestValidationError
from app.shared.base_exceptions import (
    AuthorizationException,
    DomainException,
    ApplicationException,
)
from pydantic import ValidationError

from .global_exception_handler import (
    handle_domain_exceptions,
    handle_application_exceptions,
    handle_generic_exceptions,
    handle_pydantic_validation_errors,
    handle_generic_exceptions,
    handle_path_validation_errors,
    handle_auth_exceptions,
    handle_value_errors,
)

exception_handlers: Any = {
    DomainException: handle_domain_exceptions,
    ApplicationException: handle_application_exceptions,
    Exception: handle_generic_exceptions,
    ValidationError: handle_pydantic_validation_errors,
    Exception: handle_generic_exceptions,
    RequestValidationError: handle_path_validation_errors,
    AuthorizationException: handle_auth_exceptions,
    ValueError: handle_value_errors,
}
