from typing import Optional, Dict, Any
from http import HTTPStatus


class AuthErrorCode:
    """Machine-readable codes for authentication and authorization failures."""

    INVALID_TOKEN = "INVALID_TOKEN"
    MISSING_BEARER = "MISSING_BEARER"
    AUTHENTICATION_REQUIRED = "AUTHENTICATION_REQUIRED"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"


AUTH_ERROR_MESSAGES: dict[str, str] = {
    AuthErrorCode.INVALID_TOKEN: "Invalid token.",
    AuthErrorCode.MISSING_BEARER: "Not authenticated.",
    AuthErrorCode.AUTHENTICATION_REQUIRED: "Authentication required.",
    AuthErrorCode.USER_NOT_FOUND: "User not found.",
    AuthErrorCode.INVALID_CREDENTIALS: "Invalid token or credentials.",
    AuthErrorCode.INSUFFICIENT_PERMISSIONS: "Insufficient permissions.",
}


class DomainException(Exception):
    """Base class for all domain-specific exceptions."""
    status_code = HTTPStatus.BAD_REQUEST
    
    def __init__(
        self,
        message: str = "A domain-specific error occurred.",
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details
        super().__init__(self.message)

class ApplicationException(Exception):
    """Base class for all application-specific exceptions."""
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR 
    
    def __init__(
        self,
        message: str = "An application error occurred.",
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details
        super().__init__(self.message)


class NotFoundException(DomainException):
    status_code = HTTPStatus.NOT_FOUND
    
    def __init__(self, entity: str, entity_id: Any):
        super().__init__(
            message=f"{entity} with ID {entity_id} not found",
            error_code=f"{entity.upper()}_NOT_FOUND",
            details={"entity": entity, "id": entity_id}
        )

class ValidationException(DomainException):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    
    def __init__(self, field: str, reason: str):
        super().__init__(
            message=f"Validation failed for field '{field}'",
            error_code="VALIDATION_ERROR",
            details={"field": field, "reason": reason}
        )


class ForbiddenException(DomainException):
    status_code = HTTPStatus.FORBIDDEN

    def __init__(
        self,
        message: str = "Access denied.",
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code or "FORBIDDEN",
            details=details,
        )


class DatabaseException(ApplicationException):
    status_code = HTTPStatus.SERVICE_UNAVAILABLE
    
    
class AuthorizationException(Exception):
    """Base class for all auth-specific exceptions."""
    status_code = HTTPStatus.UNAUTHORIZED
    
    def __init__(
        self,
        message: str = "A auth-specific error occurred.",
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details if details is not None else {}
        super().__init__(self.message)


def auth_error(
    code: str,
    *,
    message: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
) -> AuthorizationException:
    """Build a standardized auth failure (use with ``raise``)."""
    return AuthorizationException(
        message=message or AUTH_ERROR_MESSAGES.get(code, "Authentication failed."),
        error_code=code,
        details=details if details is not None else {},
    )


def forbidden_error(
    code: str = AuthErrorCode.INSUFFICIENT_PERMISSIONS,
    *,
    message: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
) -> ForbiddenException:
    """Build a standardized forbidden response (use with ``raise``)."""
    return ForbiddenException(
        message=message or AUTH_ERROR_MESSAGES.get(code, "Access denied."),
        error_code=code,
        details=details if details is not None else {},
    )
