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


class ApplicationException(Exception):
    """Internal application failure — details hidden from clients (5xx)."""

    def __init__(
        self,
        message: str,
        *,
        error_code: str = "APPLICATION_ERROR",
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
