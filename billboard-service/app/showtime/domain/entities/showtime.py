from pydantic import Field, ValidationError
from typing import Dict, List, Optional, ClassVar, Any
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from ..value_objects import Seats
from ..exceptions import *
from .base import ShowtimeBase
from ..enums import ShowtimeStatus


class Showtime(ShowtimeBase):
    """Full domain entity for a Showtime, including DB-generated fields and derived properties."""

    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    total_seats: Optional[int] = 0  # Will be derived/calculated by use case
    available_seats: int = 0  # Will be derived/calculated by use case
    seats: List[Seats] = Field(
        [], description="List of individual seat statuses for this showtime."
    )  # Derived/calculated

    class Config:
        from_attributes = True
        use_enum_values = True

    _EXTRA_DURATIONS: ClassVar = {
        "initial_cleaning": 10,
        "initial_commercials": 40,
        "post_credits_scene": 10,
        "post_cleaning": 30,
    }

    def draft(self, **kwargs):
        """
        Create an instance of Showtime with default values for created_at, updated_at, total_seats, available_seats, status, seats.
        """
        now_utc = datetime.now(timezone.utc)

        return Showtime(
            created_at=now_utc,
            updated_at=now_utc,
            total_seats=None,
            available_seats=0,
            status=ShowtimeStatus.DRAFT,
            seats=[],
            **kwargs,
        )

    def mark_as_launchable(self):
        """
        Launches a showtime.
        """
        if self.status != ShowtimeStatus.DRAFT:
            raise ValidationError("Showtime is not draft can't be launched")

        self.status = ShowtimeStatus.UPCOMING
        self.updated_at = datetime.now(timezone.utc)

    def launch(self):
        """
        Public action to launch a showtime.
        Kept as an explicit method because use cases call `launch()`.
        """
        self.mark_as_launchable()

    def cancel(self):
        """
        Cancels a showtime when it is not already completed or deleted.
        """
        if self.deleted_at is not None:
            raise ShowtimeCancellationError(self.id if self.id else 0)
        if self.status == ShowtimeStatus.COMPLETED:
            raise ShowtimeCancellationError(self.id if self.id else 0)

        self.status = ShowtimeStatus.CANCELLED
        self.updated_at = datetime.now(timezone.utc)

    def restore(self):
        """
        Restores a deleted showtime.
        """
        if self.deleted_at is None:
            raise ShowtimeRestorationError(self.id if self.id else 0)

        self.deleted_at = None
        self.updated_at = datetime.now(timezone.utc)

    def mark_as_deleted(self):
        """
        Marks the showtime as deleted.
        """
        if not self._is_deletable():
            raise ShowtimeDeletionError(self.id if self.id else 0)

        self.deleted_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def _is_deletable(self) -> bool:
        """
        Checks if the showtime is deletable.
        """
        return self.status == ShowtimeStatus.DRAFT

    def is_upcoming(self) -> bool:
        """
        Checks if the showtime has not started yet (its start time is in the future).
        Returns:
            True if the showtime's start time is after the current time, False otherwise.
        """
        # TODO: ADD TOLERANCE
        return datetime.now(timezone.utc) < self.start_time

    @classmethod
    def get_buffered_extra_times(
        cls, include_post_credits_scene: bool = False
    ) -> Dict[str, timedelta]:
        """
        Calculates the pre-show and post-show buffer durations.

        Args:
            include_post_credits_scene (bool): If True, adds time for post-credits scenes
                                               to the post-show buffer.

        Returns:
            Dict[str, timedelta]: A dictionary containing 'pre_buffer' and 'post_buffer'
                                  as timedelta objects.
        """
        pre_buffer_minutes = (
            cls._EXTRA_DURATIONS["initial_cleaning"]
            + cls._EXTRA_DURATIONS["initial_commercials"]
        )

        post_buffer_minutes = cls._EXTRA_DURATIONS["post_cleaning"]
        if include_post_credits_scene:
            post_buffer_minutes += cls._EXTRA_DURATIONS["post_credits_scene"]

        pre_buffer = timedelta(minutes=pre_buffer_minutes)
        post_buffer = timedelta(minutes=post_buffer_minutes)

        return {"pre_buffer": pre_buffer, "post_buffer": post_buffer}

    def validate_business_logic(self):
        """
        Validates the business rules for a Showtime entity.
        Raises custom domain exceptions if validation fails.
        """
        self._validate_price()
        self._validate_duration()
        self._validate_schedule_date()

    def take_seats(self, seats_number: int):
        self._validate_seat_quantity(seats_number)
        self._validate_avaliable_seats(seats_number)

        self.available_seats -= seats_number

    def _validate_seat_quantity(self, seats_number: int):
        """
        Validates seats allowed range quantity
        """
        MIN_SEAT_ALLOWED = 1
        MAX_SEAT_ALLOWED = 15

        if not MIN_SEAT_ALLOWED <= seats_number <= MAX_SEAT_ALLOWED:
            raise ShowtimeSeatsError(
                "Invalid seat quantity. "
                + f"Seat quantity must be between {MIN_SEAT_ALLOWED} to {MAX_SEAT_ALLOWED}"
            )

    def _validate_avaliable_seats(self, seats_number: int):
        """
        Validates enough quantity of a avaliable seats
        """
        if seats_number > self.available_seats:
            raise ShowtimeSeatsError("No Seats Avaliable for requested operation")

    def _validate_price(self):
        """
        Validates that the showtime price is within the allowed limits.
        """
        MAX_LIMIT_PRICE = Decimal("50.00")
        MIN_LIMIT_PRICE = Decimal("3.00")

        if not (MIN_LIMIT_PRICE < self.price < MAX_LIMIT_PRICE):
            raise InvalidShowtimePriceError(
                self.price, MIN_LIMIT_PRICE, MAX_LIMIT_PRICE
            )

    def _validate_schedule_date(self):
        """
        Validates that the showtime start_time is not in the past
        and is within a defined future limit (e.g., 30 days from now).
        """
        self._validate_not_schedule_in_past()
        self._validate_schedule_date_no_too_far()

    def _validate_duration(self):
        """
        Validates the showtime's duration, including start and end times.
        """
        MIN_SHOWTIME_DURATION_MINS = 30  # 0.5 hour (Supporting Short Films)
        MAX_SHOWTIME_DURATION_MINS = 300  # 5 hours (Supporting Sport Events)

        if not self.end_time:
            return

        if self.end_time <= self.start_time:
            raise ShowtimeSchedulingError("Showtime end time must be after start time.")

        duration_timedelta: timedelta = self.end_time - self.start_time
        duration_in_minutes = int(duration_timedelta.total_seconds() / 60)

        if not (
            MIN_SHOWTIME_DURATION_MINS
            <= duration_in_minutes
            <= MAX_SHOWTIME_DURATION_MINS
        ):
            raise InvalidShowtimeDurationError(
                duration_in_minutes,
                MIN_SHOWTIME_DURATION_MINS,
                MAX_SHOWTIME_DURATION_MINS,
            )

    def _validate_not_schedule_in_past(self):
        now_utc = datetime.now(timezone.utc)

        start_time_utc = self._normalize_datetime_to_utc(self.start_time)
        if start_time_utc < now_utc:
            raise ShowtimeSchedulingError(
                f"Showtime start time '{self.start_time.isoformat()}' cannot be in the past relative to current time."
            )

    def _validate_schedule_date_no_too_far(self):
        MAX_DAYS_START_DATE_ALLOWED = 30
        now_utc = datetime.now(timezone.utc)
        future_limit_date = now_utc + timedelta(days=MAX_DAYS_START_DATE_ALLOWED)

        start_time_utc = self._normalize_datetime_to_utc(self.start_time)
        if start_time_utc > future_limit_date:
            raise ShowtimeSchedulingError(
                f"Showtime start time '{self.start_time.isoformat()}' exceeds the maximum allowed future booking period of {MAX_DAYS_START_DATE_ALLOWED} days. "
                f"It must be before '{future_limit_date.isoformat()}'."
            )

    def _normalize_datetime_to_utc(self, dt: datetime) -> datetime:
        """
        Ensures a datetime object is timezone-aware and converted to UTC.
        If naive, it's assumed to be UTC. If aware, it's converted to UTC.
        """
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        else:
            return dt.astimezone(timezone.utc)
