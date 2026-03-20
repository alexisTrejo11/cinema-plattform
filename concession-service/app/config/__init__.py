from typing import Any
import asyncio

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.shared.base_exceptions import (
    AuthorizationException,
    DomainException,
    ApplicationException,
)

from app.config.logging import setup_logging
from .app_config import settings
from .registry_service import RegistryMicroservice

import logging


logger = logging.getLogger("app")

from .global_exception_handler import (
    handle_domain_exceptions,
    handle_application_exceptions,
    handle_auth_exceptions,
    handle_pydantic_validation_errors,
    handle_path_validation_errors,
    handle_db_exceptions,
    handle_value_errors,
    handle_generic_exceptions,
)

exception_handlers: Any = {
    DomainException: handle_domain_exceptions,
    ApplicationException: handle_application_exceptions,
    AuthorizationException: handle_auth_exceptions,
    ValidationError: handle_pydantic_validation_errors,
    RequestValidationError: handle_path_validation_errors,
    SQLAlchemyError: handle_db_exceptions,
    ValueError: handle_value_errors,
    AttributeError: handle_value_errors,
    Exception: handle_generic_exceptions,
}
