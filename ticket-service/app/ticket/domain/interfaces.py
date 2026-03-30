from abc import ABC, abstractmethod
from typing import List, Optional
from app.ticket.application.dtos import SearchTicketParams
from app.ticket.domain.entities import Ticket, ShowtimeSeat


class TicketRepository(ABC):
    """Abstract base class defining the interface for ticket repository implementations.

    This interface provides the contract for all ticket persistence operations,
    ensuring consistent behavior across different repository implementations
    (e.g., SQL, NoSQL, in-memory).
    """

    @abstractmethod
    async def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        """Retrieve a single ticket by its unique identifier.

        Args:
            ticket_id: The unique identifier of the ticket to retrieve

        Returns:
            Optional[Ticket]: The ticket if found, None otherwise

        Raises:
            RepositoryError: If there's an error accessing the data store
        """
        pass

    @abstractmethod
    async def list_by_user_id(self, user_id: int) -> List[Ticket]:
        """Retrieve all tickets associated with a specific user.

        Args:
            user_id: The unique identifier of the user

        Returns:
            List[Ticket]: A list of tickets belonging to the user,
                         empty list if none found

        Raises:
            RepositoryError: If there's an error accessing the data store
        """
        pass

    @abstractmethod
    async def list_by_showtime_id(self, showtime_id: int) -> List[Ticket]:
        """Retrieve all tickets for a specific showtime.

        Args:
            showtime_id: The unique identifier of the showtime

        Returns:
            List[Ticket]: A list of tickets for the showtime,
                         empty list if none found

        Raises:
            RepositoryError: If there's an error accessing the data store
        """
        pass

    @abstractmethod
    async def search(self, search_params: SearchTicketParams) -> List[Ticket]:
        """Search tickets based on various filtering criteria.

        Args:
            search: SearchTicketParams object containing all filter,
                   pagination, and sorting parameters

        Returns:
            List[Ticket]: A list of tickets matching the search criteria,
                         empty list if none found

        Raises:
            RepositoryError: If there's an error accessing the data store
            ValueError: If invalid search parameters are provided
        """
        pass

    @abstractmethod
    async def save(self, ticket: Ticket) -> Ticket:
        """Persist a ticket entity in the repository.

        Args:
            ticket: The ticket entity to save/create

        Returns:
            Ticket: The saved ticket entity with any generated fields
                    (e.g., ID, timestamps) populated

        Raises:
            RepositoryError: If there's an error accessing the data store
            ConcurrentModificationError: If version conflict occurs
        """
        pass

    @abstractmethod
    async def delete(self, ticket_id: int) -> bool:
        """Delete a ticket from the repository.

        Args:
            ticket_id: The unique identifier of the ticket to delete

        Returns:
            bool: True if the ticket was deleted, False if no ticket
                  was found with the given ID

        Raises:
            RepositoryError: If there's an error accessing the data store
        """
        pass


class SeatRepository(ABC):
    """Persistence for per-showtime seat rows (local replica; gRPC asserts authority)."""

    @abstractmethod
    async def get_by_id_and_showtime(
        self, showtime_id: int, id: int
    ) -> Optional[ShowtimeSeat]:
        pass

    @abstractmethod
    async def list_by_id_in(self, id_list: List[int]) -> List[ShowtimeSeat]:
        pass

    async def get_by_id_in(self, id_list: List[int]) -> List[ShowtimeSeat]:
        return await self.list_by_id_in(id_list)

    @abstractmethod
    async def list_by_showtime(self, showtime_id: int) -> List[ShowtimeSeat]:
        pass

    async def get_by_showtime(self, showtime_id: int) -> List[ShowtimeSeat]:
        return await self.list_by_showtime(showtime_id)

    @abstractmethod
    async def list_by_showtime_and_id_in(
        self, showtime_id: int, showtime_seat_ids: List[int]
    ) -> List[ShowtimeSeat]:
        """IDs are `showtime_seats.id` values for the given showtime."""
        pass

    async def get_by_showtime_and_id_in(
        self, showtime_id: int, seat_id_in: List[int]
    ) -> List[ShowtimeSeat]:
        return await self.list_by_showtime_and_id_in(showtime_id, seat_id_in)

    @abstractmethod
    async def save(self, seat: ShowtimeSeat) -> ShowtimeSeat:
        pass

    @abstractmethod
    async def bulk_create(self, seats: List[ShowtimeSeat]) -> None:
        pass

    @abstractmethod
    async def bulk_update(self, seats: List[ShowtimeSeat]) -> None:
        pass
