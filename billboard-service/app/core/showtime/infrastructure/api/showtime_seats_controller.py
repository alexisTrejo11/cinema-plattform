from typing import List
from fastapi import APIRouter, Depends, Request
from app.core.showtime.domain.entities.showtime_seat import ShowtimeSeat
from app.config.jwt_auth_middleware import AuthenticatedUserDTO, require_roles
from .dependencies import (
    CancelSeatUseCase,
    TakeSeatUseCase,
    ListShowtimeSeatsUseCase,
    GetShowtimeSeatByIdUseCase,
)
from .dependencies import (
    cancel_showtime_seat_use_case,
    take_showtime_seat_use_case,
    list_showtimes_seat_use_case,
    get_showtime_seat_use_case,
)
import logging

logger = logging.getLogger("app")
router = APIRouter(prefix="/api/v1/showtimes", tags=["Showtime Seats"])


@router.get("/{showtime_id}/seats", response_model=List[ShowtimeSeat])
async def list_showtime_seat_disponibility(
    request: Request,
    showtime_id: int,
    usecase: ListShowtimeSeatsUseCase = Depends(list_showtimes_seat_use_case),
) -> List[ShowtimeSeat]:
    logger.info(
        f"LIST seats started | showtime_id:{showtime_id} | client:{request.client.host if request.client else None}"
    )
    try:
        showtime_seats = await usecase.execute(showtime_id)
        logger.info(
            f"LIST seats success | showtime_id:{showtime_id} | count:{len(showtime_seats)}"
        )
        return showtime_seats
    except Exception as e:
        logger.error(f"LIST seats failed | showtime_id:{showtime_id} | error:{str(e)}")
        raise


@router.get("/{showtime_id}/seats/{seat_id}", response_model=ShowtimeSeat)
async def get_showtime_seat(
    seat_id: int,
    request: Request,
    showtime_id: int,
    usecase: GetShowtimeSeatByIdUseCase = Depends(get_showtime_seat_use_case),
) -> ShowtimeSeat:
    logger.info(
        f"GET seat started | showtime_id:{showtime_id} | seat_id:{seat_id} | client:{request.client.host if request.client else None}"
    )
    try:
        showtime_seat = await usecase.execute(showtime_id, seat_id)
        logger.info(f"GET seat success | showtime_id:{showtime_id} | seat_id:{seat_id}")
        return showtime_seat
    except Exception as e:
        logger.error(
            f"GET seat failed | showtime_id:{showtime_id} | seat_id:{seat_id} | error:{str(e)}"
        )
        raise


@router.patch("/seats/{seat_id}/take", response_model=ShowtimeSeat)
async def take_seat(
    seat_id: int,
    request: Request,
    showtime_id: int,
    usecase: TakeSeatUseCase = Depends(take_showtime_seat_use_case),
    current_user: AuthenticatedUserDTO = Depends(require_roles("admin", "manager")),
):
    logger.info(
        f"TAKE seat started | showtime_id:{showtime_id} | seat_id:{seat_id} | actor:{current_user.user_id} | roles:{current_user.roles} | client:{request.client.host if request.client else None}"
    )
    try:
        showtime_seat = await usecase.execute(showtime_id, seat_id)
        logger.info(
            f"TAKE seat success | showtime_id:{showtime_id} | seat_id:{seat_id}"
        )
        return showtime_seat
    except Exception as e:
        logger.error(
            f"TAKE seat failed | showtime_id:{showtime_id} | seat_id:{seat_id} | error:{str(e)}"
        )
        raise


@router.patch("/seats/{seat_id}/cancel", response_model=ShowtimeSeat)
async def cancel_seat(
    request: Request,
    seat_id: int,
    showtime_id: int,
    usecase: CancelSeatUseCase = Depends(cancel_showtime_seat_use_case),
    current_user: AuthenticatedUserDTO = Depends(require_roles("admin", "manager")),
):
    logger.info(
        f"CANCEL seat started | showtime_id:{showtime_id} | seat_id:{seat_id} | actor:{current_user.user_id} | roles:{current_user.roles} | client:{request.client.host if request.client else None}"
    )
    try:
        showtime_seat = await usecase.execute(showtime_id, seat_id)
        logger.info(
            f"CANCEL seat success | showtime_id:{showtime_id} | seat_id:{seat_id}"
        )
        return showtime_seat
    except Exception as e:
        logger.error(
            f"CANCEL seat failed | showtime_id:{showtime_id} | seat_id:{seat_id} | error:{str(e)}"
        )
        raise
