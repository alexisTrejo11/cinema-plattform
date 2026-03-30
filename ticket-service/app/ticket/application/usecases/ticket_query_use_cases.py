import logging
from typing import List

from app.ticket.application.dtos import SearchTicketParams, TicketResponse

from app.ticket.domain.services import TicketService

_log = logging.getLogger("app.ticket.application")


class GetTicketByIdUseCase:
    def __init__(self, ticket_service: TicketService) -> None:
        self.ticket_service = ticket_service

    async def execute(self, ticket_id: int) -> TicketResponse:
        ticket = await self.ticket_service.get_ticket_by_id(ticket_id)
        _log.info("ticket_get_by_id", extra={"props": {"ticket_id": ticket_id}})
        return TicketResponse(**ticket.to_dict())


class GetTicketsByUserIdUseCase:
    """
    -Retrieves tickets based on user id.
    -Used by admins or registred users that want to see their ticket history
    """

    def __init__(self, ticket_service: TicketService) -> None:
        self.ticket_service = ticket_service

    async def execute(
        self, user_id: int, verbose: bool = False
    ) -> List[TicketResponse]:
        tickets = await self.ticket_service.get_user_tickets(user_id)
        return [TicketResponse(**ticket.to_dict()) for ticket in tickets]


class GetTicketsByShowtimeIdUseCase:
    """
    -Retrieves tickets based on showtime.
    -One ticket will be retrived for each seat to show availability
    """

    def __init__(self, ticket_service: TicketService) -> None:
        self.ticket_service = ticket_service

    async def execute(
        self, showtime_id: int, include_seats: bool = True
    ) -> List[TicketResponse]:
        tickets = await self.ticket_service.get_showtime_tickets(showtime_id)
        return [TicketResponse(**ticket.to_dict()) for ticket in tickets]


class GetTicketsByCriteriaUseCase:
    def __init__(self, ticket_service: TicketService) -> None:
        self.ticket_service = ticket_service

    async def execute(self, search_params: SearchTicketParams) -> List[TicketResponse]:
        tickets = await self.ticket_service.search_tickets(search_params)
        _log.info(
            "tickets_search",
            extra={"props": {"count": len(tickets)}},
        )
        return [TicketResponse(**ticket.to_dict()) for ticket in tickets]
