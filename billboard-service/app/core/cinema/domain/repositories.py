from typing import Optional, List, TYPE_CHECKING
from abc import abstractmethod, ABC
from app.core.shared.repository.common_repository import CommonRepository
from app.core.shared.pagination import PaginationParams, Page
from app.core.cinema.domain.entities import Cinema

if TYPE_CHECKING:
    from app.core.cinema.application.dtos import SearchCinemaFilters


class CinemaRepository(CommonRepository[Cinema], ABC):
    """
    Specific repository interface for Cinema entities.
    Inherits common CRUD methods for Cinema.
    """

    @abstractmethod
    async def find_by_tax_number(self, tax_number: str) -> Optional[Cinema]:
        pass

    @abstractmethod
    async def find_active(self, params: PaginationParams) -> Page[Cinema]:
        """
        Find active cinemas with pagination.

        Args:
            params: Pagination parameters (offset, limit, sort_by, sort_order)

        Returns:
            Page[Cinema] with active cinemas and pagination metadata
        """
        pass

    @abstractmethod
    async def search(
        self, params: PaginationParams, filters: "SearchCinemaFilters"
    ) -> Page[Cinema]:
        """
        Perform a dynamic search of cinemas with pagination and filtering capabilities.

        Args:
            params: Pagination parameters (offset, limit, sort_by, sort_order)
            filters: Filter criteria for cinemas

        Returns:
            Page[Cinema] with filtered cinemas and pagination metadata
        """
        pass

    @abstractmethod
    async def count_active(self) -> int:
        """
        Count total number of active cinemas.
        """
        pass

    @abstractmethod
    async def restore(self, entity_id: int) -> None:
        pass

    @abstractmethod
    async def is_deleted(self, entity_id: int) -> bool:
        pass
