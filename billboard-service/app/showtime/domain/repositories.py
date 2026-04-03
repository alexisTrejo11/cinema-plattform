from typing import Dict, List, Optional, TYPE_CHECKING
from datetime import datetime
from abc import abstractmethod, ABC
from app.shared.core.pagination import PaginationParams, Page
from app.showtime.domain.entities.showtime import Showtime
from app.showtime.domain.entities.showtime_seat import ShowtimeSeat
from app.movies.application.dtos import MovieShowtimesFilters

if TYPE_CHECKING:
    from app.showtime.application.dtos import SearchShowtimeFilters


class ShowTimeRepository(ABC):
    @abstractmethod
    async def find_incoming_by_cinema(self, cinema_id: int) -> List[Showtime]:
        pass

    @abstractmethod
    async def find_incoming_by_movie(self, movie_id: int) -> List[Showtime]:
        pass

    @abstractmethod
    async def find_by_filters_group_by_movie(
        self, showtime_filters: MovieShowtimesFilters, page_data: PaginationParams
    ) -> Dict[int, List[Showtime]]:
        pass

    @abstractmethod
    async def find_by_theater_and_date_range(
        self,
        theater_id: int,
        start_time_to_check: datetime,
        end_time_to_check: datetime,
        exclude_showtime_id: Optional[int] = None,
    ) -> List[Showtime]:
        pass

    @abstractmethod
    async def search(
        self, params: PaginationParams, filters: "SearchShowtimeFilters"
    ) -> Page[Showtime]:
        """
        Search showtimes with filters and pagination.

        Args:
            params: Pagination parameters (offset, limit, sort_by, sort_order)
            filters: Filter criteria for showtimes

        Returns:
            Page[Showtime] with filtered showtimes and pagination metadata
        """
        pass

    @abstractmethod
    async def find_deleted_by_id(self, showtime_id: int) -> Optional[Showtime]:
        """
        Finds a deleted showtime by its ID.
        Args:
            showtime_id: The ID of the showtime to find.
        Returns:
            The deleted showtime if found, otherwise None.
        """
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
    async def find_by_showtime(self, showtime_id: int) -> List[ShowtimeSeat]:
        pass

    @abstractmethod
    async def bulk_create(self, seats: List[ShowtimeSeat]) -> None:
        pass

    @abstractmethod
    async def save(self, seat: ShowtimeSeat) -> ShowtimeSeat:
        pass
