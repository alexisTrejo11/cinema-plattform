from typing import List
from app.core.shared.exceptions import NotFoundException
from app.core.theater.domain.seat import TheaterSeat
from .dtos import TheaterSeatCreate, TheaterSeatUpdate
from .repositories import TheaterRepository, TheaterSeatRepository
from .mappers import TheaterSeatMapper as SeatMappers
from .seat_validation_service import SeatValidationService


class GetTheaterSeatByIdUseCase:
    """
    Use case to retrieve a single theater seat by its ID.
    """

    def __init__(self, repository: TheaterSeatRepository):
        self.repository = repository

    async def execute(self, seat_id: int) -> TheaterSeat:
        """
        Executes the use case to find a theater seat.

        Args:
            seat_id: The unique identifier of the theater seat.

        Returns:
            The TheaterSeat if found, otherwise None.
        """
        seat = await self.repository.get_by_id(seat_id)
        if not seat:
            raise NotFoundException("Seat", seat_id)

        return seat


class GetSeatsByTheaterUseCase:
    """
    Use case to retrieve all theater seats for a specific theater.
    """

    def __init__(
        self,
        seat_repository: TheaterSeatRepository,
        theater_repository: TheaterRepository,
    ):
        self.seat_repository = seat_repository
        self.theater_repository = theater_repository

    async def execute(self, theater_id: int) -> List[TheaterSeat]:
        """
        Executes the use case to find all seats in a given theater.

        Args:
            theater_id: The unique identifier of the theater.

        Returns:
            A list of TheaterSeat objects.
        """
        theater = await self.theater_repository.get_by_id(theater_id)
        if not theater:
            raise NotFoundException("Theater", theater_id)

        return await self.seat_repository.get_by_theater(theater_id)


class CreateTheaterSeatUseCase:
    def __init__(
        self,
        seat_repository: TheaterSeatRepository,
        validation_service: SeatValidationService,
    ):
        self.seat_repository = seat_repository
        self.validation_service = validation_service

    async def execute(self, seat_data: TheaterSeatCreate) -> TheaterSeat:
        await self.validation_service.validate_seat_create(seat_data)
        new_seat = SeatMappers.from_create_request(seat_data)
        return await self.seat_repository.save(new_seat)


class UpdateTheaterSeatUseCase:
    def __init__(
        self,
        seat_repository: TheaterSeatRepository,
        validation_service: SeatValidationService,
    ):
        self.seat_repository = seat_repository
        self.validation_service = validation_service

    async def execute(
        self, seat_id: int, update_data: TheaterSeatUpdate
    ) -> TheaterSeat:
        existing_seat = await self._get_seat(seat_id)
        await self.validation_service.validate_seat_update(update_data)

        updated_seat = SeatMappers.from_update_dto(update_data, existing_seat)
        existing_seat.id = seat_id

        return await self.seat_repository.save(updated_seat)

    async def _get_seat(self, seat_id: int):
        theater = await self.seat_repository.get_by_id(seat_id)
        if not theater:
            raise NotFoundException("Seat", seat_id)

        return theater


class DeleteTheaterSeatUseCase:
    """
    Use case to delete a theater seat by its ID.
    """

    def __init__(self, repository: TheaterSeatRepository):
        self.repository = repository

    async def execute(self, seat_id: int) -> None:
        """
        Executes the use case to delete a theater seat.

        Args:
            seat_id: The unique identifier of the theater seat to delete.
        """
        seat = await self.repository.get_by_id(seat_id)
        if not seat:
            raise NotFoundException("Seat", seat_id)

        await self.repository.delete(seat_id)
