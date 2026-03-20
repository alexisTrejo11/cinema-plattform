from typing import List, Dict, Any
from app.core.cinema.domain.entities import Cinema
from app.core.cinema.domain.repositories import CinemaRepository
from app.core.cinema.domain.exceptions import CinemaNotFound
from app.core.shared.pagination import Page, PaginationParams
from .dtos import (
    CreateCinemaRequest,
    UpdateCinemaRequest,
    SearchCinemaFilters,
)
from .cache import (
    cache_active_cinemas,
    cache_cinema_by_id,
    cache_search_cinemas,
    invalidate_cinema_cache,
)


class GetCinemaByIdUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository

    @cache_cinema_by_id()
    async def execute(self, cinema_id: int) -> Cinema:
        cinema = await self.repository.find_by_id(cinema_id)
        if not cinema:
            raise CinemaNotFound("Cinema", cinema_id)

        return cinema


class SearchCinemasUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository

    @cache_search_cinemas()
    async def execute(
        self, params: PaginationParams, filters: SearchCinemaFilters
    ) -> Page[Cinema]:
        return await self.repository.search(params, filters)


class ListActiveCinemasUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository

    @cache_active_cinemas()
    async def execute(self, params: PaginationParams) -> Page[Cinema]:
        return await self.repository.find_active(params)


class CreateCinemaUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository

    @invalidate_cinema_cache()
    async def execute(self, request_data: CreateCinemaRequest) -> Cinema:
        cinema = Cinema.model_validate(request_data)

        created_cinema = await self.repository.save(cinema)

        return created_cinema


class UpdateCinemaUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository

    @invalidate_cinema_cache()
    async def execute(
        self, cinema_id: int, update_request: UpdateCinemaRequest
    ) -> Cinema:
        cinema = await self.repository.find_by_id(cinema_id)
        if not cinema:
            raise CinemaNotFound("Cinema", cinema_id)

        update_data = update_request.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(cinema, key, value)

        return await self.repository.save(cinema)


class DeleteCinemaUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository

    @invalidate_cinema_cache()
    async def execute(self, cinema_id: int) -> None:
        cinema_exists = await self.repository.exists_by_id(cinema_id)
        if not cinema_exists:
            raise CinemaNotFound("Cinema", cinema_id)

        await self.repository.delete(cinema_id)


class RestoreCinemaUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository

    @invalidate_cinema_cache()
    async def execute(self, cinema_id: int) -> None:
        is_deleted = await self.repository.is_deleted(cinema_id)
        if not is_deleted:
            raise CinemaNotFound("Cinema", cinema_id)

        await self.repository.restore(cinema_id)
