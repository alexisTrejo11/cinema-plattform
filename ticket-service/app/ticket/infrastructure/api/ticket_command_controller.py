from fastapi import APIRouter, Depends, status
from app.shared.api_reponse import ApiResponse
from app.ticket.application.dtos import BuyTicketsRequest, TicketBuyedResponse
from .depencies import buy_ticket_uc, use_ticket_uc, cancel_ticket_uc
from .depencies import buy_ticket_uc, DigitalBuyTicketsUseCase, UseTicketUseCase, CancelTicketCase
from fastapi import status, HTTPException
from typing import Annotated
from fastapi import Depends, Path
from app.ticket.application.exceptions import TicketNotFoundError, TicketInvalidOperationError

router = APIRouter(prefix="/v2/api/tickets")

@router.post("/buy", response_model=ApiResponse[TicketBuyedResponse], status_code=201)
async def buy_tickets(
    ticket_data: BuyTicketsRequest,
    use_cases: DigitalBuyTicketsUseCase = Depends(buy_ticket_uc)
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
                        "message": "Ticket Successfully Cancelled"
                    }
                }
            }
        },
        404: {
            "description": "Ticket not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Ticket not found"
                    }
                }
            }
        },
        400: {
            "description": "Invalid operation",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Cannot cancel already used ticket"
                    }
                }
            }
        }
    }
)
async def cancel_ticket(
    ticket_id: Annotated[int, Path( ..., description="The ID of the ticket to cancel", json_schema_extra={"example": 12345}, gt=0)],
    ticket_use_cases: CancelTicketCase = Depends(cancel_ticket_uc)
) -> ApiResponse[None]:
    """
    Cancel a specific ticket by ID.

    This endpoint:
    - Marks the ticket status as CANCELLED
    - Releases any associated seats for rebooking
    - Updates the ticket's updated_at timestamp

    **Prerequisites**:
    - Ticket must exist
    - Ticket must not be already used
    - User must have permission to cancel ticket

    **Business Rules**:
    - Cancellations may be subject to time limits (check showtime start time)
    - Some ticket types may be non-refundable
    """
    try:
        await ticket_use_cases.execute(ticket_id)
        return ApiResponse.success(message="Ticket Successfully Cancelled")
    except TicketNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    except TicketInvalidOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
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
                        "message": "Ticket Successfully Used"
                    }
                }
            }
        },
        404: {
            "description": "Ticket not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Ticket not found"
                    }
                }
            }
        },
        400: {
            "description": "Invalid operation",
            "content": {
                "application/json": {
                    "examples": {
                        "already_used": {
                            "value": {
                                "detail": "Ticket already used"
                            }
                        },
                        "cancelled": {
                            "value": {
                                "detail": "Cannot use cancelled ticket"
                            }
                        }
                    }
                }
            }
        }
    }
)
async def use_ticket(
    ticket_id: Annotated[int, Path(..., description="The ID of the ticket to mark as used", json_schema_extra={"example": 12345}, gt=0)],
    ticket_use_cases: UseTicketUseCase = Depends(use_ticket_uc)
) -> ApiResponse[None]:
    """
    Mark a ticket as used when scanned at venue entry.

    This endpoint:
    - Marks the ticket status as USED
    - Updates the used_at timestamp
    - Prevents further modifications to the ticket

    **Prerequisites**:
    - Ticket must exist
    - Ticket must be in CONFIRMED status
    - Showtime must not have already started

    **Business Rules**:
    - Once marked as used, ticket cannot be cancelled or refunded
    - Operation is irreversible
    """
    try:
        await ticket_use_cases.execute(ticket_id)
        return ApiResponse.success(message="Ticket Successfully Used")
    except TicketNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except TicketInvalidOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

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
