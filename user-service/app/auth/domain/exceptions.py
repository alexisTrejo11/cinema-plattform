from app.shared.exceptions import AuthorizationException

class InvalidCredentialsException(AuthorizationException):
    pass


class TokenExpiredException(AuthorizationException):
    pass


class TokenRevokedException(AuthorizationException):
    pass