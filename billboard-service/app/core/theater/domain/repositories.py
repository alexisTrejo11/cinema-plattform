from abc import ABC, abstractmethod
from typing import List, Optional
from app.core.shared.repository.common_repository import CommonRepository
from app.core.shared.pagination import PaginationParams, Page
from app.core.theater.domain.seat import TheaterSeat
from app.core.theater.domain.theater import Theater
from app.core.theater.application.dtos import SearchTheaterFilters


class TheaterRepository(CommonRepository[Theater]):
    @abstractmethod
    async def get_by_id(self, entity_id: int) -> Optional[Theater]:
        pass

    @abstractmethod
    async def list_all(self, page_params: dict) -> List[Theater]:
        pass

    @abstractmethod
    async def list_by_cinema(self, cinema_id: int) -> List[Theater]:
        pass

    @abstractmethod
    async def search(self, params: PaginationParams, filters: SearchTheaterFilters) -> Page[Theater]:
        pass


class TheaterSeatRepository(ABC):
    """
    Abstract Base Class for TheaterSeatRepository.
    Defines the contract for operations related to TheaterSeat entities.
    """

    @abstractmethod
    async def get_by_id(self, seat_id: int) -> Optional[TheaterSeat]:
        """
        Retrieves a single TheaterSeat by its unique ID.
        Args:
            seat_id: The ID of the theater seat.
        Returns:
            The TheaterSeat if found, otherwise None.
        """
        pass

    @abstractmethod
    async def exist_by_theater_and_seat_values(
        self, theater_id: int, seat_row: str, seat_number: int
    ) -> bool:
        """
        Checks if a seat with the given theater_id, seat_row, and seat_number exists.
        """
        pass

    @abstractmethod
    async def get_by_theater(self, theater_id: int) -> List[TheaterSeat]:
        """
        Retrieves all TheaterSeatEntities belonging to a specific theater.
        Args:
            theater_id: The ID of the theater.
        Returns:
            A list of TheaterSeat objects.
        """
        pass

    @abstractmethod
    async def exists_by_theater(self, theater_id: int) -> bool:
        """
        Checks if any theater seats exist for a given theater ID.
        """
        pass

    @abstractmethod
    async def save(self, seat: TheaterSeat) -> TheaterSeat:
        """
        Saves a TheaterSeat to the persistence layer.
        If the entity has an ID, it attempts to update an existing record.
        If the ID is None, it creates a new record.
        Args:
            seat: The TheaterSeat object to save.
        Returns:
            The saved TheaterSeat, potentially with an updated ID or timestamps.
        Raises:
            RuntimeError: If the save operation fails.
        """
        pass

    @abstractmethod
    async def delete(self, seat_id: int) -> None:
        """
        Deletes a TheaterSeat by its unique ID.
        Args:
            seat_id: The ID of the theater seat to delete.
        """
        pass
