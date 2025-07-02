from abc import ABC, abstractmethod
from typing import List, Optional
from app.ticket.domain.entities.ticket import Ticket, TicketStatus

class TicketRepository(ABC):
    @abstractmethod
    async def get_by_id(self, ticket_id: int, raise_excpetion=True) -> Optional[Ticket]:
        pass

    @abstractmethod
    async def list_by_user_id(self, user_id: int) -> List[Ticket]:
        pass

    @abstractmethod
    async def list_by_showtime_id(self, showtime_id: int) -> List[Ticket]:
        pass

    #@abstractmethod
    #async def list_reserved_seats(self, showtime_id: int) -> List[str]:
    #    pass

    #@abstractmethod
    #async def list_by_status(self, status: TicketStatus) -> List[Ticket]:
    #    pass

    @abstractmethod
    async def save(self, ticket: Ticket) -> Ticket:
        pass

    @abstractmethod
    async def bulk_create(self, ticket: List[Ticket]) -> None:
        pass

    @abstractmethod
    async def bulk_update(self, ticket: List[Ticket]) -> None:
        pass

    @abstractmethod
    async def delete(self, ticket_id: int) -> bool:
        pass

