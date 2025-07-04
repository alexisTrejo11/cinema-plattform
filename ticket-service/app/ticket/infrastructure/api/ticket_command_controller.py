from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from datetime import datetime


router = APIRouter(prefix="/v2/api/tickets")

@router.post("/buy", response_model=TicketResponseDTO, status_code=201)
async def buy_tickets(
    ticket_data: CreateTicketDTO,
    ticket_use_cases: TicketUseCases = Depends(ticket_use_cases)
):
    """Reservate/Buy Tickets with Validation Payment???"""
    ticket_details = await ticket_use_cases.create_ticket(ticket_data)
    return ticket_details

@router.patch("/{ticket_id}/cancel", response_model=TicketResponseDTO)
async def cancel_ticket(
    ticket_id: int,
    ticket_use_cases: TicketUseCases = Depends(ticket_use_cases)
):
    """Cancel a ticket"""
    return await ticket_use_cases.cancel_ticket(ticket_id)


@router.patch("/{ticket_id}/use", response_model=TicketResponseDTO)
async def use_ticket(
    ticket_id: int,
    ticket_use_cases: TicketUseCases = Depends(ticket_use_cases)
):
    """Mark ticket as used"""
    return await ticket_use_cases.use_ticket(ticket_id)


@router.post("/{ticket_id}/refund", response_model=RefundResponseDTO)
async def refund(
    ticket_id: int,
    refund_data: RefundRequestDTO,
    showtime_start: datetime = Query(..., description="Showtime start datetime"),
    ticket_use_cases: TicketUseCases = Depends(ticket_use_cases)
):
    """Process ticket refund"""
    return await ticket_use_cases.process_refund(ticket_id, showtime_start)


@router.patch("/{ticket_id}/deactivate", status_code=204)
async def deactivate(
    ticket_id: int,
    ticket_use_cases: TicketUseCases = Depends(ticket_use_cases)
):
    """Delete a ticket (admin only)"""
    # This would typically require admin authentication
    success = await ticket_use_cases.ticket_repository.delete(ticket_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found")
