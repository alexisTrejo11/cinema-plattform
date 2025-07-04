from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from datetime import datetime
from .depencies import buy_ticket_uc, use_ticket_uc, cancel_ticket_uc
from .depencies import buy_ticket_uc, BuyTicketsUseCase, UseTicketUseCase, CancelTicketCase
from app.ticket.application.dtos import BuyTicketsRequest, TicketBuyedResponse, TicketDetailResponse

router = APIRouter(prefix="/v2/api/tickets")

@router.post("/buy", response_model=TicketBuyedResponse, status_code=201)
async def buy_tickets(
    ticket_data: BuyTicketsRequest,
    use_cases: BuyTicketsUseCase = Depends(buy_ticket_uc)
):
    """Reservate/Buy Tickets with Validation Payment???"""
    ticket_details = await use_cases.execute(ticket_data)
    return ticket_details

@router.patch("/{ticket_id}/cancel", response_model=TicketDetailResponse)
async def cancel_ticket(
    ticket_id: int,
    ticket_use_cases: CancelTicketCase = Depends(cancel_ticket_uc)
):
    """Cancel a ticket"""
    return await ticket_use_cases.execute(ticket_id, "")


@router.patch("/{ticket_id}/use", response_model=TicketDetailResponse)
async def use_ticket(
    ticket_id: int,
    ticket_use_cases: UseTicketUseCase = Depends(use_ticket_uc)
):
    """Mark ticket as used"""
    return await ticket_use_cases.execute(ticket_id)


@router.post("/{ticket_id}/refund")
async def refund(
    ticket_id: int,
    ticket_use_cases: CancelTicketCase = Depends(cancel_ticket_uc)
):
    """Process ticket refund"""
    await ticket_use_cases.execute(ticket_id, "")

"""
@router.patch("/{ticket_id}/deactivate", status_code=204)
async def deactivate(
    ticket_id: int,
    ticket_use_cases: TicketUseCases = Depends(ticket_use_cases)
):
    # This would typically require admin authentication
    success = await ticket_use_cases.ticket_repository.delete(ticket_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found")

"""
