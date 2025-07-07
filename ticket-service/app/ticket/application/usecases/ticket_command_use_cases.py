import asyncio
from datetime import timedelta
from typing import List, Tuple
from notification.notification_service import NotificationService
from app.shared.qr import generate_ticket_qr
from app.seats.application.seat_service import ShowtimeSeatService
from app.billboard_data.domain.entities.showtime import Showtime
from app.billboard_data.application.repositories.showtime_repository import ShowtimeRepository
from app.seats.domain.showtime_seat import ShowtimeSeat
from app.ticket.domain.entities.ticket import Ticket
from ..dtos import BuyTicketsRequest, TicketPurchasedResponse, SeatInfo  
from ..service.ticket_service import TicketService
from ..exceptions import TicketNotFoundError

class DigitalBuyTicketsUseCase:
    """
    - Reservate/Taked some tickets for any customer after a payment . 
    - Could by a register customer of for anonimus customer.
    - Digital Buy: Sell it on web page an users can buy tickets in any selected cinema 
    """
    def __init__(
        self, 
        ticket_service: TicketService, 
        notification_service: NotificationService, 
        seat_service: ShowtimeSeatService, 
        showtime_repo: ShowtimeRepository
    ) -> None:
        self.ticket_service = ticket_service
        self.seat_service = seat_service
        self.showtime_repo = showtime_repo
        self.notification_service = notification_service
    
    async def execute(self, buy_dto: BuyTicketsRequest) -> TicketPurchasedResponse:
        showtime, showtime_seats =  await self._get_showtime_data(buy_dto)
        ticket_created = await self._process_ticket(buy_dto, showtime, showtime_seats)
        
        notification_coroutine = self.notification_service.send_notification_from_ticket(ticket_created, buy_dto.user_email)                 
        ticket_response_coroutine = self._generate_ticket_response(ticket_created, showtime)
        tickect_response ,_ = asyncio.gather(ticket_response_coroutine, notification_coroutine)
        
        return tickect_response
        
    async def _get_showtime_data(self, buy_dto: BuyTicketsRequest) -> Tuple[Showtime, List[ShowtimeSeat]] :
        seats_coroutine = self.seat_service.list_by_showtime_id_and_seat_id_list(buy_dto.showtime_id, buy_dto.seat_list_id)        
        showtime_coroutine = self.showtime_repo.get_by_id(buy_dto.showtime_id)
        
        showtime_seats, showtime = await asyncio.gather(seats_coroutine, showtime_coroutine)
        return showtime, showtime_seats
    
    async def _process_ticket(self, buy_dto: BuyTicketsRequest, showtime: Showtime, seats: List[ShowtimeSeat]):
        take_seats_coroutine = self.seat_service.take_seats(buy_dto.seat_list_id)
        ticket_coroutine = self.ticket_service.create_ticket(showtime, buy_dto)
        
        _, ticket = await asyncio.gather(take_seats_coroutine, ticket_coroutine)
        ticket.seats = seats
        return ticket
    
    async def _generate_ticket_response(self, ticket: Ticket, showtime: Showtime) -> TicketPurchasedResponse:
        qr = generate_ticket_qr(str(ticket.id), showtime.get_start_time() + timedelta(minutes=30))
        seat_info = [SeatInfo(**seat.to_dict()) for seat in ticket.seats] 
        
        # Add Builder
        return TicketPurchasedResponse(
            ticket_id=ticket.id,
            seats=seat_info,
            movie_name=showtime.get_movie().get_title(),
            cinema_name=showtime.get_cinema().name,
            theather_name=showtime.get_theater().get_name(),
            showtime_date=showtime.get_start_time(),
            ticket_qr=qr,
            transaction_id=str(ticket.payment_details.id),
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