from typing import Any, Literal


class DomainException(Exception):
    """Business rule violation — safe to expose to clients (4xx)."""

    def __init__(
        self,
        message: str,
        *,
        error_code: str = "DOMAIN_ERROR",
        status_code: int = 400,
        details: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details


class applicationException(Exception):
    """Internal application failure — details hidden from clients (5xx)."""

    def __init__(
        self,
        message: str,
        *,
        error_code: str = "application_ERROR",
        status_code: int = 500,
        details: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details


class AuthorizationException(Exception):
    """Auth / permission failure."""

    def __init__(
        self,
        message: str,
        *,
        error_code: str = "AUTHORIZATION_ERROR",
        status_code: int = 403,
        details: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details


# ── Helper functions for AuthorizationExceptions ───────────────────────────────────────

AuthErrorCode = Literal[
    "AUTH_ERROR", "AUTH_TOKEN_EXPIRED", "AUTH_TOKEN_INVALID", "AUTH_TOKEN_UNSUPPORTED"
]


def auth_error(error_code: AuthErrorCode, message: str = "") -> AuthorizationException:
    return AuthorizationException(
        message=message,
        error_code=error_code,
        status_code=401,
    )


def forbidden_error(
    error_code: AuthErrorCode, message: str = ""
) -> AuthorizationException:
    return AuthorizationException(
        message=message,
        error_code=error_code,
        status_code=403,
    )


class NotFoundException(DomainException):
    def __init__(self, entity_name: str, entity_id: Any, id_name: str = "id"):
        sid = str(entity_id)
        super().__init__(
            f"{entity_name} with {id_name} {sid} was not found.",
            error_code=f"{entity_name.upper()}_NOT_FOUND",
            status_code=404,
            details={"entity": entity_name, "id": sid},
        )


class ValidationException(DomainException):
    def __init__(self, field: str, reason: str):
        super().__init__(
            f"Validation failed for field '{field}': {reason}",
            error_code="VALIDATION_ERROR",
            status_code=400,
            details={"field": field, "reason": reason},
        )


class ConflictException(DomainException):
    def __init__(self, message: str, *, details: dict | None = None):
        super().__init__(
            message,
            error_code="CONFLICT",
            status_code=409,
            details=details or {},
        )
