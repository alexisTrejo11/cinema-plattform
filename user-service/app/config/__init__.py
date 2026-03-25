from typing import Any

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.shared.exceptions import (
    ApplicationException,
    AuthorizationException,
    DomainException,
)

from .global_exception_handler import (
    handle_auth_exceptions,
    handle_application_exceptions,
    handle_db_exceptions,
    handle_domain_exceptions,
    handle_generic_exceptions,
    handle_http_exceptions,
    handle_path_validation_errors,
    handle_pydantic_validation_errors,
)

exception_handlers: Any = {
    DomainException: handle_domain_exceptions,
    ApplicationException: handle_application_exceptions,
    AuthorizationException: handle_auth_exceptions,
    RequestValidationError: handle_path_validation_errors,
    ValidationError: handle_pydantic_validation_errors,
    SQLAlchemyError: handle_db_exceptions,
    HTTPException: handle_http_exceptions,
    Exception: handle_generic_exceptions,
}
