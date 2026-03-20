from app.core.shared.exceptions import NotFoundException, ValidationException
from app.core.theater.application.dtos import TheaterSeatCreate, TheaterSeatUpdate
from app.core.theater.domain.repositories import (
    TheaterSeatRepository,
    TheaterRepository,
)


class SeatValidationService:
    def __init__(
        self,
        seat_repository: TheaterSeatRepository,
        theater_repository: TheaterRepository,
    ):
        self.seat_repository = seat_repository
        self.theater_repository = theater_repository

    async def validate_seat_create(self, seat_data: TheaterSeatCreate) -> None:
        await self.validate_theater(seat_data.theater_id)
        await self.validate_not_duplicated_seat(
            seat_data.theater_id, seat_data.seat_row, seat_data.seat_number
        )

    async def validate_seat_update(self, seat_data: TheaterSeatUpdate) -> None:
        if not seat_data.theater_id:
            return

        await self.validate_theater(seat_data.theater_id)

        if not seat_data.seat_row or not seat_data.seat_number:
            return

        await self.validate_not_duplicated_seat(
            seat_data.theater_id, seat_data.seat_row, seat_data.seat_number
        )

    async def validate_theater(self, theater_id: int) -> None:
        if theater_id:
            theater = await self.theater_repository.get_by_id(theater_id)
            if not theater:
                raise NotFoundException("Theater", theater_id)

    async def validate_not_duplicated_seat(
        self, theater_id: int, seat_row: str, seat_number: int
    ):
        is_seat_duplicated = (
            await self.seat_repository.exist_by_theater_and_seat_values(
                theater_id=theater_id, seat_row=seat_row, seat_number=seat_number
            )
        )
        if is_seat_duplicated:
            raise ValidationException(
                field="Seat row-number",
                reason="Seat row-number already exists in this theater",
            )
