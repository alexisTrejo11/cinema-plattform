from typing import Optional
from http import HTTPStatus
from datetime import datetime
from app.shared.exceptions import DomainException


class ShowtimeValidationException(DomainException):
    """Base class for showtime validation exceptions"""

    status_code = HTTPStatus.UNPROCESSABLE_ENTITY


class NoSeatsInTheaterException(ShowtimeValidationException):
    """Raised when trying to create a showtime in a theater with no seats"""

    def __init__(self, theater_id: int):
        super().__init__(
            message=f"Theater {theater_id} has no seats configured",
            error_code="NO_THEATER_SEATS",
            details={
                "theater_id": theater_id,
                "reason": "Cannot create showtime in a theater with no seats",
            },
        )


class ShowtimeOverlapException(ShowtimeValidationException):
    """Raised when a proposed showtime overlaps with existing ones"""

    def __init__(
        self,
        proposed_showtime_id: Optional[int],
        existing_showtime_id: int,
        theater_id: int,
        buffered_start: datetime,
        buffered_end: datetime,
        overlap_count: int,
    ):
        super().__init__(
            message=f"Showtime scheduling conflict in theater {theater_id}",
            error_code="SHOWTIME_OVERLAP",
            details={
                "proposed_showtime_id": proposed_showtime_id,
                "existing_showtime_id": existing_showtime_id,
                "theater_id": theater_id,
                "buffered_time_range": {
                    "start": buffered_start.isoformat(),
                    "end": buffered_end.isoformat(),
                },
                "overlap_count": overlap_count,
                "reason": "Showtime buffers overlap with existing showtime",
            },
        )


class InvalidShowtimeDurationException(ShowtimeValidationException):
    """Raised when showtime duration is invalid"""

    def __init__(self, min_duration: int, max_duration: int, actual_duration: int):
        super().__init__(
            message=f"Showtime duration {actual_duration} minutes is invalid",
            error_code="INVALID_DURATION",
            details={
                "min_duration_minutes": min_duration,
                "max_duration_minutes": max_duration,
                "actual_duration_minutes": actual_duration,
                "reason": f"Duration must be between {min_duration} and {max_duration} minutes",
            },
        )


class TheaterNotFoundException(ShowtimeValidationException):
    """Raised when referenced theater doesn't exist"""

    def __init__(self, theater_id: int):
        super().__init__(
            message=f"Theater {theater_id} not found",
            error_code="THEATER_NOT_FOUND",
            details={
                "theater_id": theater_id,
                "reason": "Cannot schedule showtime in non-existent theater",
            },
        )
