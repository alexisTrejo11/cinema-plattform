from typing import Any
from app.shared.base_exceptions import DomainException, ApplicationException
from pydantic import ValidationError

from .global_exception_handler import (
    handle_domain_exceptions,
    handle_application_exceptions,
    handle_generic_exceptions,
    handle_pydantic_validation_errors,
    handle_generic_exceptions,
)

exception_handlers: Any = {
    DomainException: handle_domain_exceptions,
    ApplicationException: handle_application_exceptions,
    Exception: handle_generic_exceptions,
    ValidationError: handle_pydantic_validation_errors,
    Exception: handle_generic_exceptions,
}
