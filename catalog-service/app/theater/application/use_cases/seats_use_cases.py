from typing import List

from app.shared.core.exceptions import NotFoundException
from app.theater.domain.repositories import (
    TheaterRepository,
    TheaterSeatRepository,
)
from app.theater.domain.services import SeatValidationService
from app.theater.domain.seat import TheaterSeat

from ..cache import cache_seat_by_id, cache_seats_by_theater, invalidate_seats_cache
from ..dtos import TheaterSeatCreate, TheaterSeatUpdate
from ..mappers import TheaterSeatMapper


class GetTheaterSeatByIdUseCase:
    """Retrieve a single theater seat by its ID."""

    def __init__(self, repository: TheaterSeatRepository):
        self.repository = repository

    @cache_seat_by_id()
    async def execute(self, seat_id: int) -> TheaterSeat:
        seat = await self.repository.get_by_id(seat_id)
        if not seat:
            raise NotFoundException("Seat", seat_id)
        return seat


class GetSeatsByTheaterUseCase:
    """Retrieve all theater seats for a specific theater."""

    def __init__(
        self,
        seat_repository: TheaterSeatRepository,
        theater_repository: TheaterRepository,
    ):
        self.seat_repository = seat_repository
        self.theater_repository = theater_repository

    @cache_seats_by_theater()
    async def execute(self, theater_id: int) -> List[TheaterSeat]:
        theater = await self.theater_repository.get_by_id(theater_id)
        if not theater:
            raise NotFoundException("Theater", theater_id)

        return await self.seat_repository.get_by_theater(theater_id)


class CreateTheaterSeatUseCase:
    """Create a new theater seat."""

    def __init__(
        self,
        seat_repository: TheaterSeatRepository,
        validation_service: SeatValidationService,
    ):
        self.seat_repository = seat_repository
        self.validation_service = validation_service

    @invalidate_seats_cache()
    async def execute(self, seat_data: TheaterSeatCreate) -> TheaterSeat:
        await self.validation_service.validate_seat_create(seat_data)
        new_seat = TheaterSeatMapper.from_create_request(seat_data)
        return await self.seat_repository.save(new_seat)


class UpdateTheaterSeatUseCase:
    """Update an existing theater seat."""

    def __init__(
        self,
        seat_repository: TheaterSeatRepository,
        validation_service: SeatValidationService,
    ):
        self.seat_repository = seat_repository
        self.validation_service = validation_service

    @invalidate_seats_cache()
    async def execute(
        self, seat_id: int, update_data: TheaterSeatUpdate
    ) -> TheaterSeat:
        existing_seat = await self._get_existing_seat(seat_id)
        await self.validation_service.validate_seat_update(update_data)

        updated_seat = TheaterSeatMapper.from_update_dto(update_data, existing_seat)
        return await self.seat_repository.save(updated_seat)

    async def _get_existing_seat(self, seat_id: int) -> TheaterSeat:
        """Helper to retrieve and validate seat existence."""
        seat = await self.seat_repository.get_by_id(seat_id)
        if not seat:
            raise NotFoundException("Seat", seat_id)
        return seat


class DeleteTheaterSeatUseCase:
    """Delete a theater seat by its ID."""

    def __init__(self, repository: TheaterSeatRepository):
        self.repository = repository

    @invalidate_seats_cache()
    async def execute(self, seat_id: int) -> None:
        seat = await self.repository.get_by_id(seat_id)
        if not seat:
            raise NotFoundException("Seat", seat_id)

        await self.repository.delete(seat_id)
