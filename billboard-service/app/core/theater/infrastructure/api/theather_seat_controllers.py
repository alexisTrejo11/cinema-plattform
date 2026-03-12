from typing import List
from fastapi import APIRouter, Depends, status, Request
from .depdencies import (
    get_seats_by_theater_use_case,
    get_theater_seat_by_id_use_case,
    create_theater_seat_use_case,
    update_theater_seat_use_case,
    delete_theater_seat_use_case,
)
from app.core.theater.application.seats_use_cases import (
    GetTheaterSeatByIdUseCase,
    GetSeatsByTheaterUseCase,
    CreateTheaterSeatUseCase,
    UpdateTheaterSeatUseCase,
    DeleteTheaterSeatUseCase,
)
from app.core.theater.application.dtos import TheaterSeatCreate, TheaterSeatUpdate
from app.core.theater.domain.seat import TheaterSeat
import logging

logger = logging.getLogger("app")
router = APIRouter(prefix="/api/v1/theaters/seats", tags=["Theater Seats"])


@router.get(
    "/{seat_id}", response_model=TheaterSeat, summary="Get a theater seat by ID"
)
async def get_theater_seat_by_id(
    request: Request,
    seat_id: int,
    use_case: GetTheaterSeatByIdUseCase = Depends(get_theater_seat_by_id_use_case),
) -> TheaterSeat:
    logger.info(
        f"GET seat started | seat_id:{seat_id} | client:{request.client.host if request.client else None}"
    )
    try:
        seat = await use_case.execute(seat_id)
        logger.info(f"GET seat success | seat_id:{seat_id}")
        return seat
    except Exception as e:
        logger.error(f"GET seat failed | seat_id:{seat_id} | error:{str(e)}")
        raise


@router.get(
    "/by_theater/{theater_id}",
    response_model=List[TheaterSeat],
    summary="Get all seats for a specific theater",
)
async def get_seats_by_theater(
    request: Request,
    theater_id: int,
    use_case: GetSeatsByTheaterUseCase = Depends(get_seats_by_theater_use_case),
) -> List[TheaterSeat]:
    logger.info(
        f"GET seats by theater started | theater_id:{theater_id} | client:{request.client.host if request.client else None}"
    )
    try:
        seats = await use_case.execute(theater_id)
        logger.info(
            f"GET seats by theater success | theater_id:{theater_id} | count:{len(seats)}"
        )
        return seats
    except Exception as e:
        logger.error(
            f"GET seats by theater failed | theater_id:{theater_id} | error:{str(e)}"
        )
        raise


@router.post(
    "/",
    response_model=TheaterSeat,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new theater seat",
)
async def create_theater_seat(
    request: Request,
    seat_data: TheaterSeatCreate,
    use_case: CreateTheaterSeatUseCase = Depends(create_theater_seat_use_case),
) -> TheaterSeat:

    logger.info(
        f"POST seat started | theater_id:{seat_data.theater_id} | client:{request.client.host if request.client else None}"
    )
    try:
        created_seat = await use_case.execute(seat_data)
        logger.info(
            f"POST seat success | seat_id:{created_seat.id} | theater_id:{created_seat.theater_id}"
        )
        return created_seat
    except Exception as e:
        logger.error(
            f"POST seat failed | theater_id:{seat_data.theater_id} | error:{str(e)}"
        )
        raise


@router.put(
    "/{seat_id}", response_model=TheaterSeat, summary="Update an existing theater seat"
)
async def update_theater_seat(
    seat_id: int,
    request: Request,
    seat_data: TheaterSeatUpdate,
    use_case: UpdateTheaterSeatUseCase = Depends(update_theater_seat_use_case),
) -> TheaterSeat:
    logger.info(
        f"PUT seat started | seat_id:{seat_id} | client:{request.client.host if request.client else None}"
    )
    try:
        updated_seat = await use_case.execute(seat_id, seat_data)
        logger.info(f"PUT seat success | seat_id:{seat_id}")
        return updated_seat
    except Exception as e:
        logger.error(f"PUT seat failed | seat_id:{seat_id} | error:{str(e)}")
        raise


@router.delete(
    "/{seat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a theater seat by ID",
)
async def delete_theater_seat(
    request: Request,
    seat_id: int,
    use_case: DeleteTheaterSeatUseCase = Depends(delete_theater_seat_use_case),
) -> None:
    logger.info(
        f"DELETE seat started | seat_id:{seat_id} | client:{request.client.host if request.client else None}"
    )
    try:
        await use_case.execute(seat_id)
        logger.info(f"DELETE seat success | seat_id:{seat_id}")
    except Exception as e:
        logger.error(f"DELETE seat failed | seat_id:{seat_id} | error:{str(e)}")
        raise
