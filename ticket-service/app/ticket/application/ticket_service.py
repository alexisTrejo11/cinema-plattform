from typing import List, Optional
from app.ticket.domain.entities.ticket import Ticket, TicketStatus, PriceDetails
from app.ticket.application.repository import TicketRepository
from app.showtime.domain.entities.showtime import Showtime
from app.showtime.application.repositories.theater_repository import TheaterRepository
from app.ticket.application.dtos import UpdateTicketData,  TicketResponse, RefundResponse
from app.showtime.domain.entities.theater import Theater


class TicketService:
    def __init__(self, ticket_repository: TicketRepository, theater_repository: TheaterRepository):
        self.ticket_repository = ticket_repository
        self.theater_repository = theater_repository 
    
    async def create_many_from_showtime(self, showtime: Showtime) -> None:
        theater = self.theater_repository.get_by_id(showtime.get_theater_id(), raise_expection=True)
        
        showtime_tickets = await self._generate_tickets(showtime, theater)
        await self.ticket_repository.bulk_create(showtime_tickets)    
        
        print(f"successfully created {len(showtime_tickets)} tickets for showtime {showtime.get_id()}")

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


    async def cancel_ticket(self, ticket_id: int) -> None:
        ticket = await self.get_ticket_by_id(ticket_id)
        
        ticket.cancel_ticket()
        await self.ticket_repository.save(ticket)


    async def use_ticket(self, ticket_id: int) -> None:
        ticket = await self.get_ticket_by_id(ticket_id)

        ticket.use_ticket()
        await self.ticket_repository.save(ticket)
        

    async def process_refund(self, ticket_id: int, showtime_start) -> RefundResponse:
        """Process ticket refund"""
        ticket = await self.ticket_repository.get_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")

        if not ticket.is_refundable(showtime_start):
            raise ValueError("Ticket is not refundable")

        refund_amount = ticket.calculate_refund_amount()
        processing_fee = ticket.price_details.price - refund_amount

        ticket.cancel_ticket()
        await self.ticket_repository.save(ticket)

        return RefundResponse(
            ticket_id=ticket_id,
            refund_amount=ticket.price_details.price,
            processing_fee=processing_fee,
            net_refund=refund_amount,
            status="processed"
        )

    async def get_showtime_tickets(self, showtime_id: int) -> List[TicketResponse]:
        """Get all tickets for a showtime"""
        tickets = await self.ticket_repository.list_by_showtime_id(showtime_id)
        return [TicketResponse.model_validate(ticket) for ticket in tickets]

    async def _generate_tickets(self, showtime : Showtime, theater: Theater) -> List[Ticket]:
        showtime_tickets = []
        showtime_price = PriceDetails(showtime.get_price(), "MXN")
        for seat in theater.get_seats():
            new_ticket = Ticket(seat=seat, price_details=showtime_price, showtime=showtime)
            showtime_tickets.append(new_ticket)
            
        return showtime_tickets