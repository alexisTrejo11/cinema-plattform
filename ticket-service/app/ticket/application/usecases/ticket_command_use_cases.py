from ..service.ticket_service import TicketService
from app.ticket.application.dtos import BuyTicketsRequest  
from app.seats.application.seat_service import ShowtimeSeatService
from app.showtime.application.repositories.showtime_repository import ShowtimeRepository
import asyncio

class BuyTicketsUseCase:
    """
    - Reservate/Taked some tickets for any customer after a payment . 
    - Could by a register customer of for anonimus customer.
    - Customers can buy tickets in 2 ways:
        -Physical buy: Sell it in ticket office for each cinema
        -Digital: buy: Sell it on web page an users can buy tickets in any selected cinema 
    """
    def __init__(self, ticket_service: TicketService, seat_service: ShowtimeSeatService, showtime_repo: ShowtimeRepository) -> None:
        self.ticket_service = ticket_service
        self.seat_service = seat_service
        self.showtime_repo = showtime_repo
    
    async def execute(self, buy_dto: BuyTicketsRequest):
        seats_coroutine = self.seat_service.list_by_showtime_id_and_seat_id_list(buy_dto.showtime_id, buy_dto.seat_list_id)        
        showtime_coroutine = self.showtime_repo.get_by_id(buy_dto.showtime_id, raise_exception=True)
        
        showtime_seats, showtime, = await asyncio.gather(seats_coroutine, showtime_coroutine)
        
        take_seats_coroutine = self.seat_service.take_seats(buy_dto.seat_list_id)
        ticket_coroutine = self.ticket_service.create_ticket(showtime, buy_dto)
        
        _, ticket = await asyncio.gather(take_seats_coroutine, ticket_coroutine)

        ticket.seats = showtime_seats

    
class UseTicketUseCase:
    def __init__(self, ticket_service: TicketService) -> None:
        self.ticket_service = ticket_service
    
    async def execute(self, ticket_id, reason: str):
        ticket = await self.ticket_service.get_ticket_by_id(ticket_id)
        if not ticket:
            raise ValueError("invalid ticket")
        
        await self.ticket_service.use_ticket(ticket)
    
    
class CancelTicketCase:
    def __init__(self, ticket_service: TicketService) -> None:
        self.ticket_service = ticket_service
    
    async def execute(self, ticket_id, reason: str):
        ticket = await self.ticket_service.get_ticket_by_id(ticket_id)
        if not ticket:
            raise ValueError("invalid ticket")
        
        await self.ticket_service.cancel_ticket(ticket)