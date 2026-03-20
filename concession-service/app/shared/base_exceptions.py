from typing import Any, Dict, Optional
from http import HTTPStatus


class DomainException(Exception):
    """Business-rule violation — maps to 4xx.
    Message and details are safe to expose to clients."""

    status_code: int = HTTPStatus.BAD_REQUEST

    def __init__(
        self,
        message: str = "A domain error occurred.",
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__.upper()
        self.details = details if details is not None else {}
        super().__init__(self.message)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(code={self.error_code!r}, message={self.message!r})"


class ApplicationException(Exception):
    """Infrastructure / application-layer failure — maps to 5xx.
    Internal details are hidden from clients by the exception handler."""

    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(
        self,
        message: str = "An application error occurred.",
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__.upper()
        self.details = details if details is not None else {}
        super().__init__(self.message)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(code={self.error_code!r}, message={self.message!r})"


class AuthorizationException(Exception):
    """Authentication / authorization failure — maps to 401/403."""

    status_code: int = HTTPStatus.UNAUTHORIZED

    def __init__(
        self,
        message: str = "Authorization failed.",
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__.upper()
        self.details = details if details is not None else {}
        super().__init__(self.message)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(code={self.error_code!r}, message={self.message!r})"


# ─── Domain-level (4xx, client-visible) ──────────────────────────────


class NotFoundException(DomainException):
    """Requested resource does not exist (404).
    Moved under DomainException because a 404 is a client-facing response
    whose message and entity context are safe — and useful — to expose."""

    status_code: int = HTTPStatus.NOT_FOUND

    def __init__(self, entity_name: str, entity_id: Any):
        super().__init__(
            message=f"{entity_name} with ID '{entity_id}' not found.",
            error_code=f"{entity_name.upper()}_NOT_FOUND",
            details={"entity": entity_name, "id": entity_id},
        )


class ValidationException(DomainException):
    """Input data violates domain validation rules (422)."""

    status_code: int = HTTPStatus.UNPROCESSABLE_ENTITY

    def __init__(
        self,
        field: Optional[str] = None,
        reason: str = "Validation failed.",
        details: Optional[Dict[str, Any]] = None,
    ):
        message = (
            f"Validation failed for field '{field}': {reason}" if field else reason
        )
        _details: Dict[str, Any] = {"reason": reason}
        if field:
            _details["field"] = field
        if details:
            _details.update(details)
        super().__init__(message=message, error_code="VALIDATION_ERROR", details=_details)


# ─── Application-level (5xx, details hidden from client) ─────────────


class DatabaseException(ApplicationException):
    """Database operation failure (503)."""

    status_code: int = HTTPStatus.SERVICE_UNAVAILABLE
