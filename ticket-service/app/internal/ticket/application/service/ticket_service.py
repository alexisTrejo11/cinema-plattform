from decimal import Decimal
from typing import List

from app.internal.ticket.application.dtos import BuyTicketsRequest, SearchTicketParams
from app.internal.ticket.application.repository import TicketRepository
from app.internal.ticket.domain.entities.ticket import Ticket
from app.internal.ticket.domain.valueobjects.helping_classes import (
    CustomerDetails,
    PriceDetails,
)

from ..exceptions import TicketInvalidOperationError, TicketNotFoundError


class TicketService:
    def __init__(self, ticket_repository: TicketRepository, theater_repository):
        self.ticket_repository = ticket_repository
        self.theater_repository = theater_repository

    async def search_tickets(self, search_params: SearchTicketParams) -> List[Ticket]:
        return await self.ticket_repository.search(search_params)

    async def create_ticket(self, showtime, dto: BuyTicketsRequest) -> Ticket:
        total = showtime.get_price() * len(dto.seat_list_id)
        showtime_price = PriceDetails(price=Decimal(str(total)), currency="MXN")
        customer_details = CustomerDetails(
            user_email=str(dto.user_email),
            id=dto.customer_id,
            customer_ip_address=dto.customer_ip,
        )

        new_ticket = Ticket(
            showtime_id=showtime.get_id(),
            movie_id=showtime.get_movie_id(),
            price_details=showtime_price,
            ticket_type=dto.ticket_type,
            customer_details=customer_details,
        )

        return await self.ticket_repository.save(new_ticket)

    async def get_ticket_by_id(self, ticket_id: int) -> Ticket:
        ticket = await self.ticket_repository.get_by_id(ticket_id)
        if not ticket:
            raise TicketNotFoundError(ticket_id)

        return ticket

    async def get_user_tickets(self, user_id: int) -> List[Ticket]:
        tickets = await self.ticket_repository.list_by_user_id(user_id)
        return tickets

    async def confirm_ticket(self, ticket_id: int) -> Ticket:
        """Confirm assitence of a reserved ticket"""
        ticket = await self.ticket_repository.get_by_id(ticket_id)
        if not ticket:
            raise TicketNotFoundError(ticket_id)

        ticket.use_ticket()
        return await self.ticket_repository.save(ticket)

    async def cancel_ticket(self, ticket: Ticket) -> None:
        if not ticket.is_cancelable():
            raise TicketInvalidOperationError("ticket status", "not cancelable")

        ticket.cancel_ticket()
        await self.ticket_repository.save(ticket)

    async def use_ticket(self, ticket: Ticket) -> None:
        ticket.use_ticket()
        await self.ticket_repository.save(ticket)

    async def get_showtime_tickets(self, showtime_id: int) -> List[Ticket]:
        return await self.ticket_repository.list_by_showtime_id(showtime_id)
