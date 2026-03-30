from typing import Annotated

from fastapi import APIRouter, Depends, Path, Request, status

from app.config.rate_limit import limiter

from app.ticket.application.dtos import BuyTicketsRequest, TicketBuyedResponse
from app.ticket.infrastructure.api.ticket_openapi import (
    COMMON_TICKET_WRITE,
    PATCH_NO_CONTENT,
    merge_responses,
)

from .depencies import (
    CancelTicketCase,
    DigitalBuyTicketsUseCase,
    UseTicketUseCase,
    buy_ticket_uc,
    cancel_ticket_uc,
    use_ticket_uc,
)

router = APIRouter(
    prefix="/api/v2/tickets",
    tags=["Tickets — commands"],
)


@router.post(
    "/buy",
    response_model=TicketBuyedResponse,
    status_code=201,
    summary="Purchase tickets",
    description=(
        "Creates a ticket after validating seats and payment context. "
        "Returns confirmation details including a QR payload for venue entry."
    ),
    response_description="Created ticket with transaction reference and seat breakdown.",
    responses=merge_responses(
        {"201": {"description": "Ticket created successfully."}},
        COMMON_TICKET_WRITE,
    ),
)
@limiter.limit("10/minute")
async def buy_tickets(
    request: Request,
    ticket_data: BuyTicketsRequest,
    use_cases: DigitalBuyTicketsUseCase = Depends(buy_ticket_uc),
) -> TicketBuyedResponse:
    return await use_cases.execute(ticket_data)


@router.patch(
    "/{ticket_id}/cancel",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel a ticket",
    description=(
        "Marks the ticket as cancelled and releases associated seats when applicable. "
        "Idempotent only when business rules allow repeated cancel."
    ),
    responses=PATCH_NO_CONTENT,
)
@limiter.limit("30/minute")
async def cancel_ticket(
    request: Request,
    ticket_id: Annotated[
        int,
        Path(
            ...,
            description="Primary key of the ticket to cancel",
            json_schema_extra={"example": 12345},
            gt=0,
        ),
    ],
    ticket_use_cases: CancelTicketCase = Depends(cancel_ticket_uc),
) -> None:
    await ticket_use_cases.execute(ticket_id)


@router.patch(
    "/{ticket_id}/use",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Mark ticket as used",
    description=(
        "Marks the ticket as used (e.g. after QR scan at the door). "
        "Cannot be applied to cancelled or already-used tickets."
    ),
    responses=PATCH_NO_CONTENT,
)
@limiter.limit("30/minute")
async def use_ticket(
    request: Request,
    ticket_id: Annotated[
        int,
        Path(
            ...,
            description="Primary key of the ticket to mark as used",
            json_schema_extra={"example": 12345},
            gt=0,
        ),
    ],
    ticket_use_cases: UseTicketUseCase = Depends(use_ticket_uc),
) -> None:
    await ticket_use_cases.execute(ticket_id)
