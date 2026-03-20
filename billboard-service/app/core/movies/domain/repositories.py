from typing import List, TYPE_CHECKING
from abc import ABC, abstractmethod
from app.core.shared.repository.common_repository import CommonRepository
from app.core.shared.pagination import PaginationParams, Page
from .entities import Movie

if TYPE_CHECKING:
    from ..application.dtos import SearchMovieFilters


class MovieRepository(CommonRepository[Movie], ABC):
    """
    Specific repository interface for Movie entities.
    Inherits common CRUD methods for Movie.
    """

    @abstractmethod
    async def find_active(self, params: PaginationParams) -> Page[Movie]:
        """
        Find active movies with pagination.

        Args:
            params: Pagination parameters (offset, limit, sort_by, sort_order)

        Returns:
            Page[Movie] with active movies and pagination metadata
        """
        pass

    @abstractmethod
    async def search(
        self, params: PaginationParams, filters: "SearchMovieFilters"
    ) -> Page[Movie]:
        """
        Search movies with filters and pagination.

        Args:
            params: Pagination parameters (offset, limit, sort_by, sort_order)
            filters: Filter criteria for movies

        Returns:
            Page[Movie] with filtered movies and pagination metadata
        """
        pass
