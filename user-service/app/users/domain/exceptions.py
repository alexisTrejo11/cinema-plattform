from app.shared.exceptions import NotFoundException, ValidationException

class UserAlreadyExistsException(ValidationException):
    pass

class UserNotFoundException(NotFoundException):
    pass

class PasswordValidationError(ValidationException):
    pass