from typing import Optional

from app.core.shared.pagination import PaginationParams, Page
from app.core.shared.exceptions import NotFoundException, ValidationException
from app.core.showtime.domain.entities import Showtime
from app.core.showtime.domain.repositories import ShowTimeRepository
from app.core.showtime.domain.services import (
    ShowtimeValidationService as ValidationService,
    ShowTimeSeatService,
)
from ..dtos import ShowtimeCreate, ShowtimeUpdate, SearchShowtimeFilters


class GetShowtimeByIdUseCase:
    """
    Use case for retrieving a showtime by its ID.
    """

    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    async def execute(self, showtime_id: int) -> Optional[Showtime]:
        """
        Execute the use case to get a showtime by ID.
        Args:
            showtime_id: The ID of the showtime to retrieve.
        Returns:
            The showtime with the specified ID, or None if not found.
        Raises:
            NotFoundException: If no showtime with the given ID exists.
        """

        showtime = await self.repository.find_by_id(showtime_id)
        if not showtime:
            raise NotFoundException("Showtime", showtime_id)

        return showtime


class SearchShowtimesUseCase:
    """
    Use case for searching showtimes with filters and pagination.
    """

    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    async def execute(
        self, params: PaginationParams, filters: SearchShowtimeFilters
    ) -> Page[Showtime]:
        """
        Execute the use case to search showtimes based on filters and pagination.
        Args:
            params: Pagination parameters.
            filters: Filters to apply to the search.
        Returns:
            A page of showtimes matching the filters and pagination.
        """
        return await self.repository.search(params, filters)


class DraftShowtimeUseCase:
    """Use case for creating a new showtime. Creates a new showtime and associated seats."""

    def __init__(
        self,
        repository: ShowTimeRepository,
        validation_service: ValidationService,
        seat_service: ShowTimeSeatService,
    ):
        self.repository = repository
        self.validation_service = validation_service
        self.seat_service = seat_service

    async def execute(
        self, showtime_data: ShowtimeCreate, has_post_credits: bool = False
    ) -> Showtime:
        """Execute the use case to create a new showtime.
        Args:
            showtime_data: The data for the new showtime.
            has_post_credits: Whether the showtime includes post-credits scenes (for validation).
        Returns:
            The newly created showtime.
        """
        proposed_showtime = Showtime.draft(**showtime_data.model_dump())

        await self.validation_service.validate_business_logic(
            proposed_showtime, has_post_credits
        )

        showtime_created = await self.repository.save(proposed_showtime)

        # TODO: Create Event and do async # Maybe rename to create showtime tickets per seat??
        await self.seat_service.create_showtimes_seats(showtime_created)

        return showtime_created


class LaunchShowtimeUseCase:
    """Use case for launching a showtime."""

    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    async def execute(self, showtime_id: int) -> Showtime:
        """
        Execute the use case to launch a showtime."""
        showtime = await self.repository.find_by_id(showtime_id)
        if not showtime:
            raise NotFoundException("Showtime", showtime_id)

        showtime.launch()
        await self.repository.save(showtime)

        return showtime


class CancelShowtimeUseCase:
    """Use case for canceling a showtime."""

    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    async def execute(self, showtime_id: int) -> Showtime:
        """
        Execute the use case to cancel a showtime."""

        showtime = await self.repository.find_by_id(showtime_id)
        if not showtime:
            raise NotFoundException("Showtime", showtime_id)

        showtime.cancel()
        await self.repository.save(showtime)

        return showtime


# TODO: Split into other use cases:
class UpdateShowtimeUseCase:
    """Use case for updating an existing showtime."""

    def __init__(
        self,
        repository: ShowTimeRepository,
        validation_service: ValidationService,
    ):
        self.repository = repository
        self.validation_service = validation_service

    async def execute(
        self,
        showtime_id: int,
        update_data: ShowtimeUpdate,
        has_post_credits: bool = False,
    ) -> Showtime:
        """
        Execute the use case to update an existing showtime.
        Args:
            showtime_id: The ID of the showtime to update.
            update_data: The data to update the showtime with.
            has_post_credits: Whether the showtime includes post-credits scenes (for validation).
        Returns:
            The updated showtime.
        Raises:
            NotFoundException: If no showtime with the given ID exists.
        """
        existing_showtime = await self.get_showtime(showtime_id)

        updated_data = update_data.model_dump(exclude_unset=True, exclude={"id"})
        for key, value in updated_data.items():
            setattr(existing_showtime, key, value)

        await self.validation_service.validate_business_logic(
            existing_showtime, has_post_credits
        )
        # Update: HANDLE SEATS await self.seat_service.create_showtimes_seats(existing_showtime)

        return await self.repository.save(existing_showtime)

    async def get_showtime(self, showtime_id: int) -> Showtime:
        showtime = await self.repository.find_by_id(showtime_id)
        if not showtime:
            raise NotFoundException("Showtime", showtime_id)

        return showtime


class DeleteShowtimeUseCase:
    """Use case for deleting an existing showtime."""

    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    async def execute(self, showtime_id: int, is_hard_delete: bool = False) -> None:
        """
        Execute the use case to delete an existing showtime.
        Args:
            showtime_id: The ID of the showtime to delete.
        Raises:
            NotFoundException: If no showtime with the given ID exists.
        """
        showtime = await self.repository.find_by_id(showtime_id)
        if not showtime:
            raise NotFoundException(f"Showtime", showtime_id)

        if is_hard_delete:
            # Called to validate if showtime is deletable
            if not showtime.mark_as_deleted():
                raise ValidationException(f"Showtime", "Showtime is not deletable")
            await self.repository.delete(showtime_id)
            return

        showtime.mark_as_deleted()
        await self.repository.save(showtime)


class RestoreShowtimeUseCase:
    """Use case for restoring a deleted showtime."""

    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    async def execute(self, showtime_id: int) -> Showtime:
        """
        Execute the use case to restore a deleted showtime.
        Args:
            showtime_id: The ID of the showtime to restore.
        Returns:
            The restored showtime.
        Raises:
            NotFoundException: If no deleted showtime with the given ID exists.
            ValidationException: If the showtime is not restorable.
        """
        showtime = await self.repository.find_deleted_by_id(showtime_id)
        if not showtime:
            raise NotFoundException("Showtime", showtime_id)

        showtime.restore()
        await self.repository.save(showtime)

        return showtime


# TODO: Add a Cron Job to cancel showtimes that are in the IN_PROGRESS and COMPLETED
