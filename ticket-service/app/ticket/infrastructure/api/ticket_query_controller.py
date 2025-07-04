from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from datetime import datetime
from .depencies import get_ticket_by_id_uc, list_ticket_by_showtime_id_uc, list_ticket_by_showtime_id_uc, list_ticket_by_user_id_uc, search_showtimes_uc
from .depencies import GetTicketByIdUseCase , SearchSearchUseCase, ListTicketsByShowtimeIdUseCase, ListTicketsByUserIdUseCase
from app.ticket.application.dtos import TicketResponse

router = APIRouter()

@router.get("/{ticket_id}", response_model=List[TicketResponse])
async def search_tickets(
    ticket_id: int,
    use_case: SearchSearchUseCase = Depends(search_showtimes_uc)
):
    ticket = await use_case.execute(None)
    return ticket



@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: int,
    use_case: GetTicketByIdUseCase = Depends(search_showtimes_uc)
):
    """Get ticket by ID"""
    ticket = await use_case.execute(ticket_id)

    return ticket


@router.get("/user/{user_id}", response_model=List[TicketResponse])
async def list_user_tickets(
    user_id: int,
    use_case: ListTicketsByUserIdUseCase = Depends(list_ticket_by_user_id_uc)
):
    return await use_case.execute(user_id)


@router.get("/showtime/{showtime_id}", response_model=List[TicketResponse])
async def list_showtime_tickets(
    showtime_id: int,
    use_case: ListTicketsByShowtimeIdUseCase = Depends(list_ticket_by_showtime_id_uc)
):
    return await use_case.execute(showtime_id)


