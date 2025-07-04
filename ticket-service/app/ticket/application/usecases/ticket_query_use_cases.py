from typing import List
from ..service.ticket_service import TicketService
from ..dtos import TicketResponse


class GetTicketByIdUseCase: 
    def __init__(self, ticket_service: TicketService) -> None:
        self.ticket_service =  ticket_service

    async def execute(self, ticket_id: int) -> TicketResponse:
        ticket = await self.ticket_service.get_ticket_by_id(ticket_id)
        return TicketResponse(**ticket.to_dict())


class SearchSearchUseCase:
    """
    -Retrieves tickets based on dynamic filters.
    -Used by admins for manual monitoring  
    """
    def __init__(self, ticket_service: TicketService) -> None:
        self.ticket_service =  ticket_service

    async def execute(self, search_params: dict) -> List[TicketResponse]:
        tickets = await self.ticket_service.search_tickets(search_params)
        return [TicketResponse(**ticket.to_dict()) for ticket in tickets]
                
                
class ListTicketsByUserIdUseCase:
    """
    -Retrieves tickets based on user id.
    -Used by admins or registred users that want to see their ticket history  
    """
    def __init__(self, ticket_service: TicketService) -> None:
            self.ticket_service =  ticket_service
    
    async def execute(self, user_id: int, verbose: bool = False) -> List[TicketResponse]:
        tickets = await self.ticket_service.get_user_tickets(user_id)
        return [TicketResponse(**ticket.to_dict()) for ticket in tickets]

    
class ListTicketsByShowtimeIdUseCase:
    """
    -Retrieves tickets based on showtime.
    -One ticket will be retrived for each seat to show availability 
    """
    def __init__(self, ticket_service: TicketService) -> None:
            self.ticket_service =  ticket_service

    async def execute(self, user_id: int) -> List[TicketResponse]:
        tickets = await self.ticket_service.get_showtime_tickets(user_id)
        return [TicketResponse(**ticket.to_dict()) for ticket in tickets]
