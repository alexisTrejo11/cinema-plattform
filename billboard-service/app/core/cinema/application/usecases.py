from typing import List, Dict, Any
from app.core.cinema.domain.entities import Cinema
from app.core.cinema.domain.exceptions import CinemaNotFound
from app.core.cinema.application.dtos import (
    CreateCinemaRequest,
    UpdateCinemaRequest,
)
from .repository import CinemaRepository
from .mappers import CinemaMapper


class GetCinemaByIdUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository

    async def execute(self, cinema_id: int) -> Cinema:
        cinema = await self.repository.find_by_id(cinema_id)
        if not cinema:
            raise CinemaNotFound("Cinema", cinema_id)

        return cinema


class SearchCinemasUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository

    async def execute(
        self, page_params: Dict[str, int], filter_params: Dict[str, Any]
    ) -> List[Cinema]:
        return await self.repository.search(page_params, filter_params)


class ListActiveCinemasUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository

    async def execute(self) -> List[Cinema]:
        return await self.repository.list_active()


class CreateCinemaUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository

    async def execute(self, create_data: CreateCinemaRequest) -> Cinema:
        new_cinema = CinemaMapper.from_create_request(create_data)

        return await self.repository.save(new_cinema)


class UpdateCinemaUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository

    async def execute(self, cinema_id: int, update_data: UpdateCinemaRequest) -> Cinema:
        existing_cinema = await self.repository.find_by_id(cinema_id)
        if not existing_cinema:
            raise CinemaNotFound("Cinema", cinema_id)

        updated_cinema = CinemaMapper.update_cinema_from_request(
            existing_cinema, update_data
        )

        return await self.repository.save(updated_cinema)


class DeleteCinemaUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository

    async def execute(self, cinema_id: int) -> None:
        cinema_exists = await self.repository.exists_by_id(cinema_id)
        if not cinema_exists:
            raise CinemaNotFound("Cinema", cinema_id)

        await self.repository.delete(cinema_id)
