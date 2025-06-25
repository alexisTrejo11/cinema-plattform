from typing import Any, Dict
from app.shared.exceptions import NotFoundException, ValidationException, ApplicationException

class UserAlreadyExistsException(ValidationException):
    pass

class UserNotFoundException(NotFoundException):
    pass


class TwoFaAlreadyConfiguredError(ApplicationException):
    def __init__(self, message: str = "An application error occurred.", error_code: str | None = None, details: Dict[str, Any] | None = None):
        super().__init__(message, error_code, details)


class User2FaAuthError(ApplicationException):
    def __init__(self, message: str = "User 2FA error", error_code: str | None = None, details: Dict[str, Any] | None = None):
        super().__init__(message, error_code, details)


class InvalidTokenError(ApplicationException):
    def __init__(self, message: str = "Invalid or Expired Token", error_code: str | None = None, details: Dict[str, Any] | None = None):
        super().__init__(message, error_code, details)


class PasswordValidationError(ValidationException):
    pass