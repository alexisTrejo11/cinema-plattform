from typing import Optional, Dict, List, Any
from app.core.theater.domain.theater import Theater
from app.core.cinema.application.repository import CinemaRepository
from app.core.shared.exceptions import NotFoundException
from ..application.repositories import TheaterRepository


class GetTheaterByIdUseCase:
    def __init__(self, repository: TheaterRepository):
        self.repository = repository

    async def execute(self, theater_id: int) -> Optional[Theater]:
        return await self.repository.get_by_id(theater_id)


class GetTheatersByCinemaUseCase:
    def __init__(self, repository: TheaterRepository):
        self.repository = repository

    async def execute(self, cinema_id: int) -> List[Theater]:
        return await self.repository.list_by_cinema(cinema_id)


class ListTheatersUseCase:
    def __init__(self, repository: TheaterRepository):
        self.repository = repository

    async def execute(self, page_params: Dict[str, Any]) -> List[Theater]:
        page_params = page_params or {"offset": 0, "limit": 100}
        theaters = await self.repository.list_all(page_params)

        return theaters


class CreateTheaterUseCase:
    def __init__(
        self, theater_repository: TheaterRepository, cinema_repository: CinemaRepository
    ):
        self.theater_repository = theater_repository
        self.cinema_repository = cinema_repository

    async def execute(self, theater: Theater) -> Theater:
        await self.validate_cinema(theater.cinema_id)
        theater.validate_buissness_rules()

        return await self.theater_repository.save(theater)

    async def validate_cinema(self, cinema_id: int):
        cinema = await self.cinema_repository.get_by_id(cinema_id)
        if not cinema:
            raise NotFoundException("Cinema", cinema_id)


class UpdateTheaterUseCase:
    def __init__(
        self, theater_repository: TheaterRepository, cinema_repository: CinemaRepository
    ):
        self.theater_repository = theater_repository
        self.cinema_repository = cinema_repository

    async def execute(self, theater_id: int, update_data: Theater) -> Theater:
        existing_theater = await self.get_theater(theater_id)
        await self.validate_cinema(update_data.cinema_id)

        existing_theater.update(update_data)
        existing_theater.validate_buissness_rules()

        return await self.theater_repository.save(existing_theater)

    async def get_theater(self, theater_id: int):
        theater = await self.theater_repository.get_by_id(theater_id)
        if not theater:
            raise NotFoundException(f"Theater", theater_id)
        return theater

    async def validate_cinema(self, cinema_id: int):
        cinema = await self.cinema_repository.get_by_id(cinema_id)
        if not cinema:
            raise NotFoundException(f"Cinema", cinema_id)


class DeleteTheaterUseCase:
    def __init__(self, repository: TheaterRepository):
        self.repository = repository

    async def execute(self, theater_id: int) -> None:
        theater = await self.repository.get_by_id(theater_id)
        if not theater:
            raise NotFoundException("Theater", theater_id)

        await self.repository.delete(theater_id)
