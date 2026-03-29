from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.internal.ticket.application.dtos import BuyTicketsRequest, TicketBuyedResponse
from app.internal.ticket.application.exceptions import (
    TicketInvalidOperationError,
    TicketNotFoundError,
)
from app.shared.api_reponse import ApiResponse

from .depencies import (
    CancelTicketCase,
    DigitalBuyTicketsUseCase,
    UseTicketUseCase,
    buy_ticket_uc,
    cancel_ticket_uc,
    use_ticket_uc,
)

router = APIRouter(prefix="/api/v2/tickets")


@router.post("/buy", response_model=ApiResponse[TicketBuyedResponse], status_code=201)
async def buy_tickets(
    ticket_data: BuyTicketsRequest,
    use_cases: DigitalBuyTicketsUseCase = Depends(buy_ticket_uc),
):
    """Reservate/Buy Tickets with Validation Payment???"""
    ticket_details = await use_cases.execute(ticket_data)
    return ApiResponse.success(ticket_details)


@router.patch(
    "/{ticket_id}/cancel",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Cancel a ticket",
    description="Marks a ticket as cancelled and releases associated seats",
    responses={
        200: {
            "description": "Ticket successfully cancelled",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Ticket Successfully Cancelled",
                    }
                }
            },
        },
        404: {
            "description": "Ticket not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Ticket not found"},
                }
            },
        },
        400: {
            "description": "Invalid operation",
            "content": {
                "application/json": {
                    "example": {"detail": "Cannot cancel already used ticket"},
                }
            },
        },
    },
)
async def cancel_ticket(
    ticket_id: Annotated[
        int,
        Path(
            ...,
            description="The ID of the ticket to cancel",
            json_schema_extra={"example": 12345},
            gt=0,
        ),
    ],
    ticket_use_cases: CancelTicketCase = Depends(cancel_ticket_uc),
) -> ApiResponse[None]:
    try:
        await ticket_use_cases.execute(ticket_id)
        return ApiResponse.success(message="Ticket Successfully Cancelled")
    except TicketNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    except TicketInvalidOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.patch(
    "/{ticket_id}/use",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Mark ticket as used",
    description="Marks a ticket as used when scanned at venue entry",
    responses={
        200: {
            "description": "Ticket successfully marked as used",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Ticket Successfully Used",
                    }
                }
            },
        },
        404: {
            "description": "Ticket not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Ticket not found"},
                }
            },
        },
        400: {
            "description": "Invalid operation",
            "content": {
                "application/json": {
                    "examples": {
                        "already_used": {
                            "value": {"detail": "Ticket already used"},
                        },
                        "cancelled": {
                            "value": {"detail": "Cannot use cancelled ticket"},
                        },
                    }
                }
            },
        },
    },
)
async def use_ticket(
    ticket_id: Annotated[
        int,
        Path(
            ...,
            description="The ID of the ticket to mark as used",
            json_schema_extra={"example": 12345},
            gt=0,
        ),
    ],
    ticket_use_cases: UseTicketUseCase = Depends(use_ticket_uc),
) -> ApiResponse[None]:
    try:
        await ticket_use_cases.execute(ticket_id)
        return ApiResponse.success(message="Ticket Successfully Used")
    except TicketNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except TicketInvalidOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
