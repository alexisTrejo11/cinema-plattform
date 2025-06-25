from typing import Any, Dict
from app.shared.exceptions import NotFoundException, ValidationException, ApplicationException

class UserAlreadyExistsException(ValidationException):
    pass

class UserNotFoundException(NotFoundException):
    pass


class TwoFaAlreadyConfiguredError(ApplicationException):
    def __init__(self, message: str = "An application error occurred.", error_code: str | None = None, details: Dict[str, Any] | None = None):
        super().__init__(message, error_code, details)


class UserDontHave2FAError(ApplicationException):
    def __init__(self, message: str = "User don't have 2fa activated", error_code: str | None = None, details: Dict[str, Any] | None = None):
        super().__init__(message, error_code, details)


class InvalidTokenError(ApplicationException):
    def __init__(self, message: str = "Invalid or Expired Token", error_code: str | None = None, details: Dict[str, Any] | None = None):
        super().__init__(message, error_code, details)


class PasswordValidationError(ValidationException):
    pass