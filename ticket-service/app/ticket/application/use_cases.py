
    
from typing import List, Optional
from app.ticket.domain.entities.ticket import Ticket, TicketStatus
from app.ticket.application.repositories import TicketRepository
from app.ticket.application.dtos import (
    CreateTicketData, 
    UpdateTicketData, 
    TicketResponse,
    RefundRequest,
    RefundResponse
)

class TicketUseCases:
    def __init__(self, ticket_repository: TicketRepository):
        self.ticket_repository = ticket_repository

    
    # TODO: Define Strategy, Maybe get Ticket Related data connecting with micorservices or manage it here
    async def create_ticket(self, dto: CreateTicketData) -> TicketResponse:
        reserved_seats = await self.ticket_repository.list_reserved_seats(dto.showtime_id)
        if dto.seat_number in reserved_seats:
            raise ValueError(f"Seat {dto.seat_number} is already reserved")

        ticket = Ticket()

        created_ticket = await self.ticket_repository.save(ticket)
        return TicketResponse.model_validate(created_ticket)

    async def get_ticket_by_id(self, ticket_id: int) -> Optional[TicketResponse]:
        ticket = await self.ticket_repository.get_by_id(ticket_id)
        if not ticket:
            return None
        
        return TicketResponse.model_validate(ticket)

    async def get_user_tickets(self, user_id: int) -> List[TicketResponse]:
        tickets = await self.ticket_repository.list_by_user_id(user_id)
        return [TicketResponse.model_validate(ticket) for ticket in tickets]

    async def confirm_ticket(self, ticket_id: int) -> TicketResponse:
        """Confirm a reserved ticket"""
        ticket = await self.ticket_repository.get_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")

        ticket.confirm_ticket()
        updated_ticket = await self.ticket_repository.save(ticket)
        return TicketResponse.model_validate(updated_ticket)

    async def cancel_ticket(self, ticket_id: int) -> TicketResponse:
        ticket = await self.ticket_repository.get_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")

        ticket.cancel_ticket()
        updated_ticket = await self.ticket_repository.save(ticket)
        
        return TicketResponse.model_validate(updated_ticket)

    async def use_ticket(self, ticket_id: int) -> TicketResponse:
        ticket = await self.ticket_repository.get_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")

        ticket.use_ticket()
        updated_ticket = await self.ticket_repository.save(ticket)
        
        return TicketResponse.model_validate(updated_ticket)

    async def process_refund(self, ticket_id: int, showtime_start) -> RefundResponse:
        """Process ticket refund"""
        ticket = await self.ticket_repository.get_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")

        if not ticket.is_refundable(showtime_start):
            raise ValueError("Ticket is not refundable")

        refund_amount = ticket.calculate_refund_amount()
        processing_fee = ticket.price - refund_amount

        ticket.cancel_ticket()
        await self.ticket_repository.save(ticket)

        return RefundResponse(
            ticket_id=ticket_id,
            refund_amount=ticket.price,
            processing_fee=processing_fee,
            net_refund=refund_amount,
            status="processed"
        )

    async def get_showtime_tickets(self, showtime_id: int) -> List[TicketResponse]:
        """Get all tickets for a showtime"""
        tickets = await self.ticket_repository.list_by_showtime_id(showtime_id)
        return [TicketResponse.model_validate(ticket) for ticket in tickets]

    async def update_ticket(self, ticket_id: int, dto: UpdateTicketData) -> TicketResponse:
        """Update ticket details"""
        ticket = await self.ticket_repository.get_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")

        if ticket.status != TicketStatus.RESERVED:
            raise ValueError("Only reserved tickets can be updated")

        if dto.seat_number:
            reserved_seats = await self.ticket_repository.list_reserved_seats(ticket.showtime.id)
            if dto.seat_number in reserved_seats and dto.seat_number != ticket.showtime.seat.number:
                raise ValueError(f"Seat {dto.seat_number} is already reserved")
            ticket.showtime.seat.number = dto.seat_number

        if dto.seat_type:
            ticket.showtime.seat.type = dto.seat_type

        updated_ticket = await self.ticket_repository.save(ticket)
        return TicketResponse.model_validate(updated_ticket)