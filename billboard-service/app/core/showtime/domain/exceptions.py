from decimal import Decimal
from app.core.shared.exceptions import DomainException


class InvalidShowtimePriceError(DomainException):
    """Exception raised when a showtime's price is outside the allowed range."""

    def __init__(self, price: Decimal, min_price: Decimal, max_price: Decimal):
        message = f"Showtime price {price:.2f} is outside the allowed range. Must be between {min_price:.2f} and {max_price:.2f}."
        super().__init__(message)
        self.price = price
        self.min_price = min_price
        self.max_price = max_price


class InvalidShowtimeDurationError(DomainException):
    """Exception raised when a showtime's duration is invalid."""

    def __init__(
        self, duration_mins: int, min_duration_mins: int, max_duration_mins: int
    ):
        message = (
            f"Showtime duration ({duration_mins} minutes) is invalid. "
            f"Must be between {min_duration_mins} and {max_duration_mins} minutes."
        )
        super().__init__(message)
        self.duration_mins = duration_mins
        self.min_duration_mins = min_duration_mins
        self.max_duration_mins = max_duration_mins


class ShowtimeSchedulingError(DomainException):
    """Exception raised for general scheduling conflicts or illogical start/end times."""

    def __init__(
        self, message: str = "Showtime start time cannot be after or equal to end time."
    ):
        super().__init__(message)


class ShowtimeSeatsError(DomainException):
    """Exception raised for general seats conflicts."""

    def __init__(
        self,
        message: str = "Showtime don't have available seats to requested operation",
    ):
        super().__init__(message)
