from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from dependency_injector.wiring import Provide, inject
from datetime import datetime

from app.application.use_cases.ticket_use_cases import TicketUseCases
from app.application.dtos.ticket_dto import (
    CreateTicketDTO,
    UpdateTicketDTO,
    TicketResponseDTO,
    TicketListResponseDTO,
    RefundRequestDTO,
    RefundResponseDTO
)
from app.infrastructure.container import Container

router = APIRouter()

@router.post("/", response_model=TicketResponseDTO, status_code=201)
@inject
async def create_ticket(
    ticket_data: CreateTicketDTO,
    ticket_use_cases: TicketUseCases = Depends(Provide[Container.ticket_use_cases])
):
    """Create a new ticket reservation"""
    try:
        return await ticket_use_cases.create_ticket(ticket_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{ticket_id}", response_model=TicketResponseDTO)
@inject
async def get_ticket(
    ticket_id: int,
    ticket_use_cases: TicketUseCases = Depends(Provide[Container.ticket_use_cases])
):
    """Get ticket by ID"""
    ticket = await ticket_use_cases.get_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.get("/user/{user_id}", response_model=List[TicketResponseDTO])
@inject
async def get_user_tickets(
    user_id: int,
    ticket_use_cases: TicketUseCases = Depends(Provide[Container.ticket_use_cases])
):
    """Get all tickets for a user"""
    return await ticket_use_cases.get_user_tickets(user_id)

@router.get("/showtime/{showtime_id}", response_model=List[TicketResponseDTO])
@inject
async def get_showtime_tickets(
    showtime_id: int,
    ticket_use_cases: TicketUseCases = Depends(Provide[Container.ticket_use_cases])
):
    """Get all tickets for a showtime"""
    return await ticket_use_cases.get_showtime_tickets(showtime_id)

@router.put("/{ticket_id}", response_model=TicketResponseDTO)
@inject
async def update_ticket(
    ticket_id: int,
    ticket_data: UpdateTicketDTO,
    ticket_use_cases: TicketUseCases = Depends(Provide[Container.ticket_use_cases])
):
    """Update ticket details"""
    try:
        return await ticket_use_cases.update_ticket(ticket_id, ticket_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{ticket_id}/confirm", response_model=TicketResponseDTO)
@inject
async def confirm_ticket(
    ticket_id: int,
    ticket_use_cases: TicketUseCases = Depends(Provide[Container.ticket_use_cases])
):
    """Confirm a reserved ticket"""
    try:
        return await ticket_use_cases.confirm_ticket(ticket_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{ticket_id}/cancel", response_model=TicketResponseDTO)
@inject
async def cancel_ticket(
    ticket_id: int,
    ticket_use_cases: TicketUseCases = Depends(Provide[Container.ticket_use_cases])
):
    """Cancel a ticket"""
    try:
        return await ticket_use_cases.cancel_ticket(ticket_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{ticket_id}/use", response_model=TicketResponseDTO)
@inject
async def use_ticket(
    ticket_id: int,
    ticket_use_cases: TicketUseCases = Depends(Provide[Container.ticket_use_cases])
):
    """Mark ticket as used"""
    try:
        return await ticket_use_cases.use_ticket(ticket_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{ticket_id}/refund", response_model=RefundResponseDTO)
@inject
async def process_refund(
    ticket_id: int,
    refund_data: RefundRequestDTO,
    showtime_start: datetime = Query(..., description="Showtime start datetime"),
    ticket_use_cases: TicketUseCases = Depends(Provide[Container.ticket_use_cases])
):
    """Process ticket refund"""
    try:
        return await ticket_use_cases.process_refund(ticket_id, showtime_start)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{ticket_id}", status_code=204)
@inject
async def delete_ticket(
    ticket_id: int,
    ticket_use_cases: TicketUseCases = Depends(Provide[Container.ticket_use_cases])
):
    """Delete a ticket (admin only)"""
    # This would typically require admin authentication
    success = await ticket_use_cases.ticket_repository.delete(ticket_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found")
