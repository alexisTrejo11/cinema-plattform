from datetime import timezone, datetime
from typing import List

from app.core.shared.exceptions import ValidationException
from app.core.theater.domain.repositories import TheaterSeatRepository
from app.core.theater.domain.seat import TheaterSeat
from app.core.showtime.domain.entities import Showtime, ShowtimeSeat
from app.core.showtime.domain.repositories import (
    ShowTimeRepository,
    ShowtimeSeatRepository,
)


class ShowtimeValidationService:
    def __init__(
        self,
        showtime_repo: ShowTimeRepository,
        theater_seat_repo: TheaterSeatRepository,
    ):
        self.showtime_repo = showtime_repo
        self.theater_seat_repo = theater_seat_repo

    async def validate_insert(
        self, proposed_showtime: Showtime, has_post_credits: bool
    ):
        await self.validate_no_overlap(proposed_showtime, has_post_credits)
        await self.validate_theater_seats(proposed_showtime.theater_id)

    async def validate_theater_seats(self, theater_id: int):
        theater_count = await self.theater_seat_repo.exists_by_theater(theater_id)
        if theater_count == 0:
            raise ValidationException(
                field="Theater", reason="Don't have seats to create showtime"
            )

    async def validate_no_overlap(
        self, proposed_showtime: Showtime, include_post_credits_scene: bool = False
    ):
        """
        Validates if a proposed showtime conflicts with any existing showtimes
        in the same theater, considering pre and post buffers.

        Args:
            proposed_showtime (Showtime): The new showtime being proposed.
            include_post_credits_scene (bool): Whether to include post-credits scene
                                               duration in the end time buffer.

        Raises:
            ValidationException: If the proposed showtime overlaps with an existing one.
        """
        buffers = Showtime.get_buffered_extra_times(include_post_credits_scene)
        pre_buffer = buffers["pre_buffer"]
        post_buffer = buffers["post_buffer"]

        buffered_start_time = proposed_showtime.start_time - pre_buffer
        buffered_end_time = proposed_showtime.end_time + post_buffer

        if not proposed_showtime.id:
            overlapping_showtimes = (
                await self.showtime_repo.list_by_theater_and_date_range(
                    theater_id=proposed_showtime.theater_id,
                    start_time_to_check=buffered_start_time,
                    end_time_to_check=buffered_end_time,
                )
            )
        else:
            overlapping_showtimes = (
                await self.showtime_repo.list_by_theater_and_date_range(
                    theater_id=proposed_showtime.theater_id,
                    start_time_to_check=buffered_start_time,
                    end_time_to_check=buffered_end_time,
                    exclude_showtime_id=proposed_showtime.id,
                )
            )

        if overlapping_showtimes:
            first_overlap = overlapping_showtimes[0]
            raise ValidationException(
                field="Starttime",
                reason=f"Can't schedule Showtime (ID: {proposed_showtime.id}). "
                + f"It overlaps with existing Showtime {first_overlap.id} "
                + f"in Theater {proposed_showtime.theater_id}. "
                + f"Proposed buffered range: {buffered_start_time.strftime('%H:%M')} - {buffered_end_time.strftime('%H:%M')}. "
                + f"Found {len(overlapping_showtimes)} overlapping showtime(s).",
            )


class ShowTimeSeatService:
    def __init__(
        self,
        theater_seat_repo: TheaterSeatRepository,
        showtime_seat_repo: ShowtimeSeatRepository,
    ):
        self.theater_seat_repo = theater_seat_repo
        self.showtime_seat_repo = showtime_seat_repo

    async def create_showtimes_seats(self, showtime: Showtime):
        theater_seats = await self.theater_seat_repo.get_by_theater(showtime.theater_id)
        showtimes_seats = self._generate_showtimes_seats(theater_seats, showtime)
        await self.showtime_seat_repo.bulk_create(showtimes_seats)

    def _generate_showtimes_seats(
        self, theater_seats: List[TheaterSeat], showtime: Showtime
    ) -> List[ShowtimeSeat]:
        showtimes_seats: List[ShowtimeSeat] = []

        for theater_seat in theater_seats:
            if showtime.id is None or theater_seat.id is None:
                raise ValueError(
                    "Showtime id and theater_seat cannot be None when creating showtime seats."
                )

            showtime_seat = ShowtimeSeat(
                showtime_id=showtime.id,
                theater_seat_id=theater_seat.id,
                id=None,
                taken_at=None,
                user_id=None,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            showtimes_seats.append(showtime_seat)

        return showtimes_seats
