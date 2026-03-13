from typing import Optional, List, Dict, Any

from app.core.shared.exceptions import NotFoundException
from app.core.shared.pagination import PaginationParams
from app.core.showtime.domain.entities import Showtime
from app.core.showtime.domain.repositories import ShowTimeRepository


class GetShowtimeByIdUseCase:
    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    async def execute(self, showtime_id: int) -> Optional[Showtime]:
        showtime = await self.repository.get_by_id(showtime_id)
        if not showtime:
            raise NotFoundException("Showtime", showtime_id)

        return showtime


class GetShowtimesUseCase:
    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    async def execute(
        self, filters: Dict[str, Any], page_params: PaginationParams
    ) -> List[Showtime]:
        showtimes = await self.repository.list_all(page_params.model_dump())

        if filters:
            showtimes = [s for s in showtimes if self._matches_filters(s, filters)]

        return showtimes

    def _matches_filters(self, showtime: Showtime, filters: Dict[str, Any]) -> bool:
        if "movie_id" in filters and showtime.movie_id != filters["movie_id"]:
            return False
        if "theater_id" in filters and showtime.theater_id != filters["theater_id"]:
            return False
        if "is_active" in filters and showtime.is_upcoming() != filters["is_active"]:
            return False
        return True
