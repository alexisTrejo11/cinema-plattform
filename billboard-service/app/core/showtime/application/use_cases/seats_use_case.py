from typing import List

from app.core.shared.exceptions import NotFoundException, ValidationException
from app.core.showtime.domain.entities.showtime_seat import ShowtimeSeat
from app.core.showtime.domain.repositories import (
    ShowtimeSeatRepository,
    ShowTimeRepository,
)


class ListShowtimeSeatsUseCase:
    def __init__(
        self, seat_repo: ShowtimeSeatRepository, showtime_repo: ShowTimeRepository
    ):
        self.seat_repo = seat_repo
        self.showtime_repo = showtime_repo

    async def execute(
        self, showtime_id: int, to_be_exhibited: bool = True
    ) -> List[ShowtimeSeat]:
        await self._validate_showtime(showtime_id, to_be_exhibited)

        showtime_seats = await self.seat_repo.list_by_showtime(showtime_id)
        return showtime_seats if (showtime_seats and len(showtime_seats) > 0) else []

    async def _validate_showtime(self, showtime_id: int, to_be_exhibited: bool):
        showtime = await self.showtime_repo.get_by_id(showtime_id)
        if not showtime:
            raise NotFoundException("Showtime", showtime_id)

        if to_be_exhibited:
            is_showtime_upcoming = showtime.is_upcoming()
            if not is_showtime_upcoming:
                raise ValidationException("Showtime", "Showtime must be incoming")


class GetShowtimeSeatByIdUseCase:
    def __init__(self, seat_repo: ShowtimeSeatRepository):
        self.seat_repo = seat_repo

    async def execute(self, showtime_id: int, seat_id: int) -> ShowtimeSeat:
        seat = await self.seat_repo.get_by_showtime_and_seat(showtime_id, seat_id)
        if not seat:
            raise NotFoundException(
                "Showtime Seat", f"showtime:{showtime_id} - seat:{seat_id}"
            )

        return seat


class TakeSeatUseCase:
    def __init__(self, seat_repo: ShowtimeSeatRepository):
        self.seat_repo = seat_repo

    async def execute(self, showtime_id: int, seat_id: int) -> ShowtimeSeat:
        seat = await self.seat_repo.get_by_showtime_and_seat(showtime_id, seat_id)
        if not seat:
            raise NotFoundException("Showtime Seat", seat_id)

        seat.take()
        await self.seat_repo.save(seat)

        return seat


class CancelSeatUseCase:
    def __init__(self, seat_repo: ShowtimeSeatRepository):
        self.seat_repo = seat_repo

    async def execute(self, showtime_id: int, seat_id: int) -> ShowtimeSeat:
        seat = await self.seat_repo.get_by_showtime_and_seat(showtime_id, seat_id)
        if not seat:
            raise NotFoundException("Showtime Seat", seat_id)

        seat.leave()
        await self.seat_repo.save(seat)

        return seat
