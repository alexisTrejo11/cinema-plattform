from typing import Annotated, List

from fastapi import APIRouter, Depends, Path, Query, Request

from app.config.rate_limit import limiter

from app.ticket.application.dtos import (
    PurchaseQuoteResponse,
    SearchTicketParams,
    SeatInfo,
    TicketResponse,
    TicketSummaryResponse,
)
from app.ticket.infrastructure.api.ticket_openapi import (
    COMMON_TICKET_READ,
    HTTP_404_JSON,
    merge_responses,
)

from .depencies import (
    GetTicketByIdUseCase,
    GetTicketsByCriteriaUseCase,
    GetTicketsByShowtimeIdUseCase,
    GetTicketsByUserIdUseCase,
    GetPurchaseQuoteUseCase,
    GetUserTicketSummaryUseCase,
    ListShowtimeSeatsForSaleUseCase,
    get_purchase_quote_uc,
    get_ticket_by_id_uc,
    get_user_ticket_summary_uc,
    list_showtime_seats_uc,
    list_ticket_by_showtime_id_uc,
    list_ticket_by_user_id_uc,
    search_showtimes_uc,
    search_ticket_params,
)

router = APIRouter(
    prefix="/api/v2/tickets",
    tags=["Tickets — queries"],
)


@router.get(
    "/user/{user_id}/summary",
    response_model=TicketSummaryResponse,
    summary="Ticket counts for a user",
    description="Aggregated totals for dashboard / account pages (active, used, cancelled).",
    responses=merge_responses(
        {
            "200": {
                "description": "Summary statistics for the user.",
            }
        },
        COMMON_TICKET_READ,
        {"404": HTTP_404_JSON},
    ),
)
@limiter.limit("60/minute")
async def get_user_ticket_summary(
    request: Request,
    user_id: Annotated[int, Path(..., description="User id", gt=0, json_schema_extra={"example": 42})],
    use_case: GetUserTicketSummaryUseCase = Depends(get_user_ticket_summary_uc),
) -> TicketSummaryResponse:
    return await use_case.execute(user_id)


@router.get(
    "/quotes/showtime/{showtime_id}",
    response_model=PurchaseQuoteResponse,
    summary="Price quote for a showtime",
    description=(
        "Read-only price preview from the replicated showtime (Mongo). "
        "Does not hold seats or create a reservation."
    ),
    responses=merge_responses(
        {"200": {"description": "Computed unit and total price for the requested seat count."}},
        COMMON_TICKET_READ,
        {"404": HTTP_404_JSON},
    ),
)
@limiter.limit("120/minute")
async def get_purchase_quote(
    request: Request,
    showtime_id: Annotated[int, Path(..., gt=0, description="Showtime identifier")],
    seat_count: int = Query(1, ge=1, le=100, description="Number of seats to price"),
    use_case: GetPurchaseQuoteUseCase = Depends(get_purchase_quote_uc),
) -> PurchaseQuoteResponse:
    return await use_case.execute(showtime_id, seat_count)


@router.get(
    "/showtime/{showtime_id}/seats",
    response_model=List[SeatInfo],
    summary="Seats available for a showtime",
    description="Seat map / availability derived from theater replica and showtime seat rows.",
    responses=merge_responses(
        {"200": {"description": "List of seats with row, number, and type."}},
        COMMON_TICKET_READ,
    ),
)
@limiter.limit("120/minute")
async def list_showtime_seats(
    request: Request,
    showtime_id: Annotated[int, Path(..., gt=0, description="Showtime identifier")],
    use_case: ListShowtimeSeatsForSaleUseCase = Depends(list_showtime_seats_uc),
) -> List[SeatInfo]:
    return await use_case.execute(showtime_id)


@router.get(
    "/",
    response_model=List[TicketResponse],
    summary="Search tickets",
    description=(
        "Filter and paginate tickets using optional movie, showtime, user, status, "
        "and date-range criteria. Sorting is best-effort depending on repository support."
    ),
    responses=merge_responses(
        {"200": {"description": "Matching tickets (may be empty)."}},
        COMMON_TICKET_READ,
    ),
)
@limiter.limit("60/minute")
async def search_tickets(
    request: Request,
    params: Annotated[SearchTicketParams, Depends(search_ticket_params)],
    use_case: GetTicketsByCriteriaUseCase = Depends(search_showtimes_uc),
) -> List[TicketResponse]:
    return await use_case.execute(params)


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse,
    summary="Get ticket by ID",
    description="Returns one ticket with optional seat breakdown when stored.",
    responses=merge_responses(
        {"200": {"description": "Ticket payload."}},
        COMMON_TICKET_READ,
        {"404": HTTP_404_JSON},
    ),
)
@limiter.limit("120/minute")
async def get_ticket(
    request: Request,
    ticket_id: Annotated[
        int,
        Path(
            ...,
            description="Ticket primary key",
            json_schema_extra={"example": 123},
            gt=0,
        ),
    ],
    use_case: GetTicketByIdUseCase = Depends(get_ticket_by_id_uc),
) -> TicketResponse:
    return await use_case.execute(ticket_id)


@router.get(
    "/user/{user_id}",
    response_model=List[TicketResponse],
    summary="List tickets for a user",
    description="Returns tickets owned by the user, newest first when supported by the repository.",
    responses=merge_responses(
        {"200": {"description": "Zero or more tickets."}},
        COMMON_TICKET_READ,
    ),
)
@limiter.limit("60/minute")
async def list_user_tickets(
    request: Request,
    user_id: Annotated[
        int,
        Path(..., description="User id", json_schema_extra={"example": 456}, gt=0),
    ],
    include_seats: bool = Query(
        False,
        description="Include seat information on each ticket",
        json_schema_extra={"example": True},
    ),
    use_case: GetTicketsByUserIdUseCase = Depends(list_ticket_by_user_id_uc),
) -> List[TicketResponse]:
    return await use_case.execute(user_id, include_seats)


@router.get(
    "/showtime/{showtime_id}",
    response_model=List[TicketResponse],
    summary="List tickets for a showtime",
    description="Useful for box office / capacity checks; may include seat payloads.",
    responses=merge_responses(
        {"200": {"description": "Zero or more tickets for the showtime."}},
        COMMON_TICKET_READ,
    ),
)
@limiter.limit("60/minute")
async def list_showtime_tickets(
    request: Request,
    showtime_id: Annotated[
        int,
        Path(..., description="Showtime id", json_schema_extra={"example": 789}, gt=0),
    ],
    include_seats: bool = Query(
        True,
        description="Include seat information on each ticket",
        json_schema_extra={"example": True},
    ),
    use_case: GetTicketsByShowtimeIdUseCase = Depends(list_ticket_by_showtime_id_uc),
) -> List[TicketResponse]:
    return await use_case.execute(showtime_id, include_seats)
