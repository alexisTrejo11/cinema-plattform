from typing import Any
from app.shared.exceptions import DomainException, ApplicationException, AuthorizationException

from .global_exception_handler import (
    handle_domain_exceptions,
    handle_application_exceptions,
    handle_auth_exceptions,
    handle_generic_exceptions
)

exception_handlers : Any = {
    DomainException: handle_domain_exceptions,
    ApplicationException: handle_application_exceptions,
    AuthorizationException: handle_auth_exceptions,
    Exception: handle_generic_exceptions
}