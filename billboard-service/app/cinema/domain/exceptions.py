from typing import Optional
from app.shared.core.exceptions import DomainException, NotFoundException


class CinemaNotFound(NotFoundException):
    pass


class CinemaError(DomainException):
    """Base exception for Cinema service related errors."""

    pass


class InvalidCinemaDataError(CinemaError):
    """Raised when provided cinema data is semantically invalid."""

    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(message)
        self.field = field


class DuplicateCinemaError(InvalidCinemaDataError):
    """Raised when a cinema with the same unique identifier already exists."""

    def __init__(self, message: str, field: str):
        super().__init__(message, field=field)


class CinemaStatusConflictError(InvalidCinemaDataError):
    """Raised when a cinema's status change conflicts with other rules."""

    def __init__(
        self,
        message: str,
        cinema_id: Optional[int] = None,
        current_status: Optional[str] = None,
    ):
        super().__init__(message)
        self.cinema_id = cinema_id
        self.current_status = current_status
