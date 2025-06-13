class DomainException(Exception):
    pass

class UserAlreadyExistsException(DomainException):
    pass

class UserNotFoundException(DomainException):
    pass

