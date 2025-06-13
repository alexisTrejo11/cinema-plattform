from app.users.domain.exceptions import DomainException

class InvalidCredentialsException(DomainException):
    pass


class TokenExpiredException(DomainException):
    pass


class TokenRevokedException(DomainException):
    pass