from typing import Dict, List, Optional
from datetime import datetime
from abc import abstractmethod
from app.core.shared.repository.common_repository import CommonRepository
from app.core.shared.pagination import PaginationParams
from app.core.showtime.domain.entities.showtime import Showtime
from app.core.showtime.domain.entities.showtime_seat import ShowtimeSeat
from app.core.movies.application.dtos import MovieShowtimesFilters


class ShowTimeRepository(CommonRepository[Showtime]):
    @abstractmethod
    async def list_incoming_by_cinema(self, cinema_id: int) -> List[Showtime]:
        pass

    @abstractmethod
    async def list_incoming_by_movie(self, movie_id: int) -> List[Showtime]:
        pass

    @abstractmethod
    async def list_by_filters_group_by_movie(
        self, showtime_filters: MovieShowtimesFilters, page_data: PaginationParams
    ) -> Dict[int, List[Showtime]]:
        pass

    @abstractmethod
    async def list_by_theater_and_date_range(
        self,
        theater_id: int,
        start_time_to_check: datetime,
        end_time_to_check: datetime,
        exclude_showtime_id: Optional[int] = None,
    ) -> List[Showtime]:
        pass


class ShowtimeSeatRepository:
    @abstractmethod
    async def get_by_id(self, seat_id: int) -> Optional[ShowtimeSeat]:
        pass

    @abstractmethod
    async def get_by_showtime_and_seat(
        self, showtime_id: int, seat_id: int
    ) -> Optional[ShowtimeSeat]:
        pass

    @abstractmethod
    async def list_by_showtime(self, showtime_id: int) -> List[ShowtimeSeat]:
        pass

    @abstractmethod
    async def bulk_create(self, seats: List[ShowtimeSeat]) -> None:
        pass

    @abstractmethod
    async def save(self, seat: ShowtimeSeat) -> ShowtimeSeat:
        pass
