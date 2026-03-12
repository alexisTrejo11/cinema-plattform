from app.core.shared.exceptions import NotFoundException
from app.core.showtime.domain.entities.showtime import Showtime
from ..service.showtime_validator_service import (
    ShowtimeValidationService as ValidationService,
)
from ..service.showtime_seat_service import ShowTimeSeatService
from ..repositories import ShowTimeRepository
from ..mappers import ShowtimeMappers
from ..dtos import ShowtimeCreate, ShowtimeUpdate


class ScheduleShowtimeUseCase:
    def __init__(
        self,
        showtime_repo: ShowTimeRepository,
        validation_service: ValidationService,
        seat_service: ShowTimeSeatService,
    ):
        self.showtime_repo = showtime_repo
        self.validation_service = validation_service
        self.seat_service = seat_service

    async def execute(
        self, showtime_data: ShowtimeCreate, has_post_credits: bool = False
    ) -> Showtime:
        proposed_showtime = ShowtimeMappers.from_create_request(showtime_data)
        await self.validation_service.validate_insert(
            proposed_showtime, has_post_credits
        )

        showtime_created = await self.showtime_repo.save(proposed_showtime)
        await self.seat_service.create_showtimes_seats(showtime_created)

        return showtime_created


class UpdateShowtimeUseCase:
    def __init__(
        self, showtime_repo: ShowTimeRepository, validation_service: ValidationService
    ):
        self.showtime_repo = showtime_repo
        self.validation_service = validation_service

    async def execute(
        self,
        showtime_id: int,
        update_data: ShowtimeUpdate,
        has_post_credits: bool = False,
    ) -> Showtime:
        existing_showtime = await self.get_showtime(showtime_id)

        showtime_updated = ShowtimeMappers.update_with_dto(
            update_data, existing_showtime
        )
        await self.validation_service.validate_insert(
            showtime_updated, has_post_credits
        )
        # Update: HANDLE SEATS await self.seat_service.create_showtimes_seats(showtime_updated)

        return await self.showtime_repo.save(showtime_updated)

    async def get_showtime(self, showtime_id: int) -> Showtime:
        showtime = await self.showtime_repo.get_by_id(showtime_id)
        if not showtime:
            raise NotFoundException("Showtime", showtime_id)

        return showtime


# TODO: Validate Delete
class DeleteShowtimeUseCase:
    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    async def execute(self, showtime_id: int) -> None:
        showtime = await self.repository.get_by_id(showtime_id)
        if not showtime:
            raise NotFoundException(f"Showtime", showtime_id)

        await self.repository.delete(showtime_id)
