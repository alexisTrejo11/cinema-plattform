from typing import List, Optional
from app.ticket.domain.entities.ticket import Ticket, PaymentDetails, PriceDetails, CustomerDetails
from app.ticket.application.repository import TicketRepository
from app.showtime.domain.entities.showtime import Showtime
from app.showtime.application.repositories.theater_repository import TheaterRepository
from app.ticket.application.dtos import BuyTicketsRequest  
from app.showtime.domain.entities.theather_seat import TheaterSeat as Seat

class TicketService:
    def __init__(self, ticket_repository: TicketRepository, theater_repository: TheaterRepository):
        self.ticket_repository = ticket_repository
        self.theater_repository = theater_repository 
    
    async def search_tickets(self, search_params: dict) -> List[Ticket]:
        return await self.ticket_repository.search(**search_params)
    
    
    async def create_ticket(self, showtime: Showtime, dto : BuyTicketsRequest) -> Ticket:
        showtime_price = PriceDetails(showtime.get_price() * len(dto.seat_list_id), "MXN")
        customer_details = CustomerDetails(dto.user_email, dto.customer_id, dto.customer_ip)
        
        new_ticket = Ticket(
            showtime_id=showtime.get_id(), 
            price_details=showtime_price,
            ticket_type=dto.ticket_type,
            customer_details=customer_details
            )
        
        return await self.ticket_repository.save(new_ticket)
    
    async def get_ticket_by_id(self, ticket_id: int) -> Ticket:
        ticket = await self.ticket_repository.get_by_id(ticket_id)
        if not ticket:
            raise ValueError("Value ID")
        
        return ticket
        
    async def get_user_tickets(self, user_id: int) -> List[Ticket]:
        tickets = await self.ticket_repository.list_by_user_id(user_id)
        return tickets

    async def confirm_ticket(self, ticket_id: int) -> Ticket:
        """Confirm assitence of a reserved ticket"""
        ticket = await self.ticket_repository.get_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")

        ticket.use_ticket()
        return await self.ticket_repository.save(ticket)

    async def cancel_ticket(self, ticket: Ticket) -> None:
        if not ticket.is_cancelable():
            raise ValueError("Ticket is not refundable")
        
        ticket.cancel_ticket()
        await self.ticket_repository.save(ticket)


    async def use_ticket(self,  ticket: Ticket) -> None:
        ticket.use_ticket()
        await self.ticket_repository.save(ticket)
        

    async def get_showtime_tickets(self, showtime_id: int, incoming=True) -> List[Ticket]:
        """Get all tickets for a showtime"""
        return await self.ticket_repository.list_by_showtime_id(showtime_id)
