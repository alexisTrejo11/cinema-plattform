from decimal import Decimal
from typing import List

from app.ticket.application.dtos import BuyTicketsRequest, SearchTicketParams
from app.ticket.domain.interfaces import TicketRepository
from app.ticket.domain.entities.ticket import Ticket
from app.ticket.domain.valueobjects.helping_classes import (
    CustomerDetails,
    PriceDetails,
)

from .exceptions import (
    TicketInvalidOperationError,
    TicketNotFoundError,
    TheaterNotFound,
    SeatInvalidIdListError,
)
from abc import ABC, abstractmethod
from typing import Any, Dict
from app.ticket.domain.entities import ShowtimeSeat
from app.ticket.domain.interfaces import SeatRepository
from app.external.billboard_data.application.repositories.theater_repository import (
    TheaterRepository,
)
from app.external.billboard_data.domain.entities.showtime import Showtime


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


class PaymentService(ABC):
    @abstractmethod
    async def request_payment(self, payment) -> Dict[str, Any]:
        pass


class ShowtimeSeatService:
    def __init__(
        self, repository: SeatRepository, theater_repository: TheaterRepository
    ) -> None:
        self.repository = repository
        self.theater_repository = theater_repository

    async def create_seats_from_showtime(self, showtime: Showtime):
        theater = await self.theater_repository.get_by_id(showtime.get_theater_id())
        if not theater:
            raise TheaterNotFound("Theater", showtime.get_theater_id())

        showtime_seats = []

        for theater_seat in theater.get_seats():
            seat_name = (
                f"{theater_seat.get_seat_row()}-{theater_seat.get_seat_number()}"
            )
            showtime_seat = ShowtimeSeat(
                showtime.get_id(),
                theater_seat.get_seat_id(),
                seat_name,
                theater_seat.get_is_active(),
            )
            showtime_seats.append(showtime_seat)

        await self.repository.bulk_create(showtime_seats)

        print(f"Successfully create {len(showtime_seats)} seats for showtime")

    async def list_by_showtime_id_and_seat_id_list(
        self, showtime_id: int, seat_id_list: List[int]
    ) -> List[ShowtimeSeat]:
        return await self.repository.list_by_showtime_and_id_in(
            showtime_id, seat_id_list
        )

    async def get_seats_by_showtime(self, showtime_id: int) -> List[ShowtimeSeat]:
        return await self.repository.list_by_showtime(showtime_id)

    async def take_seats(self, seats_id_list: List[int]) -> None:
        seats = await self.repository.list_by_id_in(seats_id_list)
        if len(seats) != len(seats_id_list):
            raise SeatInvalidIdListError("Seat Ids", "Not all ids are valid")

        for seat in seats:
            seat.ocuppy()

        return await self.repository.bulk_update(seats)

    async def release_seats(self, seats_id_list: List[int]):
        seats = await self.repository.list_by_id_in(seats_id_list)
        if len(seats) != len(seats_id_list):
            raise SeatInvalidIdListError("Invalid Seat", "Not all ids are valid")

        for seat in seats:
            seat.release()

        await self.repository.bulk_update(seats)
