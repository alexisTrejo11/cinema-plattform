from datetime import datetime
from fastapi import APIRouter, Depends, Path, Query
from typing import List, Optional
from app.shared.api_reponse import ApiResponse
from .depencies import get_ticket_by_id_uc, list_ticket_by_showtime_id_uc, list_ticket_by_user_id_uc, search_showtimes_uc
from .depencies import GetTicketByIdUseCase, SearchSearchUseCase, ListTicketsByShowtimeIdUseCase, ListTicketsByUserIdUseCase
from app.ticket.application.dtos import TicketResponse, SearchTicketParams, TicketStatus

router = APIRouter(prefix="/api/v2/tickets")

@router.get("/", response_model=ApiResponse[List[TicketResponse]])
async def search_tickets(
    movie_id: Optional[int] = Query(None, description="Filter by movie ID"),
    showtime_id: Optional[int] = Query(None, description="Filter by showtime ID"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    status: Optional[TicketStatus] = Query(None, description="Filter by ticket status"),
    include_seats: bool = Query(False, description="Include seat information"),
    created_before: Optional[datetime] = Query(None, description="Filter tickets created before this date"),
    created_after: Optional[datetime] = Query(None, description="Filter tickets created after this date"),
    page_limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    page_offset: int = Query(0, ge=0, description="Pagination offset"),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_direction_asc: bool = Query(True, description="Sort direction (True for ascending)"),
    use_case: SearchSearchUseCase = Depends(search_showtimes_uc)
):
    """
    Search tickets with various filtering options.
    
    Parameters:
    - movie_id: Filter by movie ID
    - showtime_id: Filter by showtime ID
    - user_id: Filter by user ID
    - status: Filter by ticket status (e.g., 'reserved', 'purchased', 'cancelled')
    - include_seats: Include seat information in the response
    - created_before: Filter tickets created before this date
    - created_after: Filter tickets created after this date
    - page_limit: Number of items per page (1-100)
    - page_offset: Pagination offset
    - sort_by: Field to sort by (e.g., 'created_at', 'price')
    - sort_direction_asc: Sort direction (True for ascending, False for descending)
    """
    search_params = SearchTicketParams(
        movie_id=movie_id,
        showtime_id=showtime_id,
        user_id=user_id,
        status=status,
        include_seats=include_seats,
        created_before=created_before,
        created_after=created_after,
        page_limit=page_limit,
        page_offset=page_offset,
        sort_by=sort_by,
        sort_direction_asc=sort_direction_asc
    )
    
    tickets = await use_case.execute(search_params)
    return ApiResponse.success(tickets, "Tickets successfully retrieved")

@router.get(
    "/{ticket_id}",
    response_model=ApiResponse[TicketResponse],
    summary="Get ticket by ID",
    responses={
        200: {"description": "Ticket details"},
        404: {"description": "Ticket not found"}
    }
)
async def get_ticket(
    ticket_id: int = Path(..., description="ID of the ticket to retrieve", json_schema_extra={"example": 123}),
    use_case: GetTicketByIdUseCase = Depends(get_ticket_by_id_uc)
) -> ApiResponse[TicketResponse]:
    """
    Retrieve detailed information about a specific ticket.
    
    Includes ticket metadata and associated seat information.
    """
    ticket = await use_case.execute(ticket_id)
    
    return ApiResponse.success(data=ticket, message="Ticket retrieved successfully")

@router.get(
    "/user/{user_id}",
    response_model=ApiResponse[List[TicketResponse]],
    summary="Get tickets by user ID",
    description="Retrieve all tickets associated with a specific user"
)
async def list_user_tickets(
    user_id: int = Path(..., description="ID of the user", json_schema_extra={"example": 456}),
    include_seats: bool = Query(
        False, 
        description="Include seat information",
        json_schema_extra={"example": True}
    ),
    use_case: ListTicketsByUserIdUseCase = Depends(list_ticket_by_user_id_uc)
) -> ApiResponse[List[TicketResponse]]:
    """
    List all tickets for a specific user.
    
    Returns tickets ordered by creation date (newest first).
    """
    tickets = await use_case.execute(user_id, include_seats)
    return ApiResponse.success(data=tickets, message=f"Found {len(tickets)} tickets for user {user_id}")

@router.get(
    "/showtime/{showtime_id}",
    response_model=ApiResponse[List[TicketResponse]],
    summary="Get tickets by showtime ID",
    description="Retrieve all tickets for a specific showtime"
)
async def list_showtime_tickets(
    showtime_id: int = Path(..., description="ID of the showtime", json_schema_extra={"example": 789}),
    include_seats: bool = Query(
        True, 
        description="Include seat information",
        json_schema_extra={"example": True}
    ),
    use_case: ListTicketsByShowtimeIdUseCase = Depends(list_ticket_by_showtime_id_uc)
) -> ApiResponse[List[TicketResponse]]:
    """
    List all tickets for a specific showtime.
    
    Useful for box office management and seat availability checks.
    """
    tickets = await use_case.execute(showtime_id, include_seats)
    return ApiResponse.success(data=tickets, message=f"Found {len(tickets)} tickets for showtime {showtime_id}")