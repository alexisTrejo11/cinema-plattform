from typing import List

from app.external.billboard_data.application.repositories.theater_repository import (
    TheaterRepository,
)
from app.external.billboard_data.domain.entities.showtime import Showtime
from app.ticket.domain.interfaces import SeatRepository
from app.ticket.domain.entities import ShowtimeSeat
from app.ticket.domain.exceptions import (
    TheaterNotFound,
    SeatInvalidIdListError,
)


class ShowtimeSeatUseCase:
    def __init__(
        self,
        seat_repository: SeatRepository,
        theater_repository: TheaterRepository,
    ) -> None:
        self.seat_repository = seat_repository
        self.theater_repository = theater_repository

    async def create_seats_from_showtime(self, showtime: Showtime):
        """
        Create seats for a showtime from a theater and save them to the database.

        Args:
            showtime: The showtime to create seats for.

        Returns:
            None
        """

        theater_id = showtime.get_theater().theater_id
        theater = await self.theater_repository.get_by_id(theater_id)
        if not theater:
            raise TheaterNotFound("Theater", theater_id)

        showtime_seats = []

        for theater_seat in theater.seats:
            seat_name = f"{theater_seat.seat_row}-{theater_seat.seat_number}"
            showtime_seat = ShowtimeSeat(
                showtime_id=showtime.get_id(),
                seat_id=theater_seat.seat_id,
                seat_name=seat_name,
                is_available=theater_seat.is_active,
            )
            showtime_seats.append(showtime_seat)

        await self.seat_repository.bulk_create(showtime_seats)

        print(f"Successfully create {len(showtime_seats)} seats for showtime")

    async def get_by_showtime_id_and_seat_id_list(
        self, showtime_id: int, seat_id_list: List[int]
    ) -> List[ShowtimeSeat]:
        return await self.seat_repository.get_by_showtime_and_id_in(
            showtime_id, seat_id_list
        )

    async def get_seats_by_showtime(self, showtime_id: int) -> List[ShowtimeSeat]:
        return await self.seat_repository.get_by_showtime(showtime_id)

    async def take_seats(self, seats_id_list: List[int]) -> None:
        seats = await self.seat_repository.get_by_id_in(seats_id_list)
        if len(seats) != len(seats_id_list):
            raise SeatInvalidIdListError("Seat Ids", "Not all ids are valid")

        for seat in seats:
            seat.ocuppy()

        return await self.seat_repository.bulk_update(seats)

    async def release_seats(self, seats_id_list: List[int]):
        seats = await self.seat_repository.get_by_id_in(seats_id_list)
        if len(seats) != len(seats_id_list):
            raise SeatInvalidIdListError("Invalid Seat", "Not all ids are valid")

        for seat in seats:
            seat.release()

        await self.seat_repository.bulk_update(seats)
