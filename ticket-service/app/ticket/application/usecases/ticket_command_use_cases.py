import asyncio
from datetime import timedelta
from typing import List, Tuple

from app.ticket.domain.entities import ShowtimeSeat
from app.ticket.application.dtos import (
    BuyTicketsRequest,
    SeatInfo,
    TicketPurchasedResponse,
)
from app.ticket.domain.services import TicketService, ShowtimeSeatService
from app.ticket.domain.entities.ticket import Ticket
from app.shared.qr import generate_ticket_qr

from app.ticket.domain.exceptions import TicketNotFoundError


class DigitalBuyTicketsUseCase:
    """
    - Reservate/Taked some tickets for any customer after a payment .
    - Could by a register customer of for anonimus customer.
    - Digital Buy: Sell it on web page an users can buy tickets in any selected cinema
    """

    def __init__(
        self,
        ticket_service: TicketService,
        seat_service: ShowtimeSeatService,
        showtime_repo,
    ) -> None:
        self.ticket_service = ticket_service
        self.seat_service = seat_service
        self.showtime_repo = showtime_repo

    async def execute(self, buy_dto: BuyTicketsRequest) -> TicketPurchasedResponse:
        showtime, showtime_seats = await self._get_showtime_data(buy_dto)
        ticket_created = await self._process_ticket(buy_dto, showtime, showtime_seats)

        ticket_response_coroutine = self._generate_ticket_response(
            ticket_created, showtime
        )
        tickect_response = await ticket_response_coroutine

        return tickect_response

    async def _get_showtime_data(
        self, buy_dto: BuyTicketsRequest
    ) -> Tuple[object, List[ShowtimeSeat]]:
        seats_coroutine = self.seat_service.list_by_showtime_id_and_seat_id_list(
            buy_dto.showtime_id, buy_dto.seat_list_id
        )
        showtime_coroutine = self.showtime_repo.get_by_id(buy_dto.showtime_id)

        showtime_seats, showtime = await asyncio.gather(
            seats_coroutine, showtime_coroutine
        )
        return showtime, showtime_seats

    async def _process_ticket(self, buy_dto: BuyTicketsRequest, showtime, seats):
        take_seats_coroutine = self.seat_service.take_seats(buy_dto.seat_list_id)
        ticket_coroutine = self.ticket_service.create_ticket(showtime, buy_dto)

        _, ticket = await asyncio.gather(take_seats_coroutine, ticket_coroutine)
        ticket.seats = seats
        return ticket

    async def _generate_ticket_response(
        self, ticket: Ticket, showtime
    ) -> TicketPurchasedResponse:
        qr = generate_ticket_qr(
            str(ticket.id), showtime.get_start_time() + timedelta(minutes=30)
        )
        seat_info = [SeatInfo(**seat.to_seat_info_dict()) for seat in ticket.seats]

        txn = (
            str(ticket.payment_details.transaction_id) if ticket.payment_details else ""
        )

        return TicketPurchasedResponse(
            ticket_id=ticket.id,
            seats=seat_info,
            movie_name=showtime.get_movie().get_title(),
            cinema_name=showtime.get_cinema().name,
            theather_name=showtime.get_theater().get_name(),
            showtime_date=showtime.get_start_time(),
            ticket_qr=qr,
            transaction_id=txn,
        )


class UseTicketUseCase:
    def __init__(self, ticket_service: TicketService) -> None:
        self.ticket_service = ticket_service

    async def execute(self, ticket_id):
        ticket = await self.ticket_service.get_ticket_by_id(ticket_id)
        if not ticket:
            raise TicketNotFoundError(ticket_id)

        await self.ticket_service.use_ticket(ticket)


class CancelTicketCase:
    def __init__(self, ticket_service: TicketService) -> None:
        self.ticket_service = ticket_service

    async def execute(self, ticket_id):
        ticket = await self.ticket_service.get_ticket_by_id(ticket_id)
        if not ticket:
            raise TicketNotFoundError(ticket_id)

        await self.ticket_service.cancel_ticket(ticket)
