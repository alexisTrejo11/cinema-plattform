from typing import Annotated, Any, Dict, List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, status, Request
from app.core.shared.pagination import PaginationParams
from app.core.showtime.domain.entities.showtime import Showtime
from app.core.showtime.application.dtos import ShowtimeCreate, ShowtimeUpdate
from .dependencies import (
    schedule_showtime_use_case,
    update_showtime_use_case,
    delete_showtime_use_case,
    get_showtime_by_id_use_case,
    get_showtimes_use_case,
)
from .dependencies import (
    GetShowtimeByIdUseCase,
    GetShowtimesUseCase,
    ScheduleShowtimeUseCase,
    UpdateShowtimeUseCase,
    DeleteShowtimeUseCase,
)
import logging

logger = logging.getLogger("app")
router = APIRouter(prefix="/api/v1/showtimes", tags=["showtimes"])


@router.get("/{showtime_id}", response_model=Showtime)
async def get_showtime(
    request: Request,
    showtime_id: int,
    use_case: GetShowtimeByIdUseCase = Depends(get_showtime_by_id_use_case),
):
    logger.info(
        f"GET showtime started | showtime_id:{showtime_id} | client:{request.client.host if request.client else None}"
    )
    try:
        showtime = await use_case.execute(showtime_id)
        logger.info(f"GET showtime success | showtime_id:{showtime_id}")
        return showtime
    except Exception as e:
        logger.error(
            f"GET showtime failed | showtime_id:{showtime_id} | error:{str(e)}"
        )
        raise


@router.get("/", response_model=List[Showtime])
async def list_showtimes(
    request: Request,
    movie_id: Annotated[Optional[int], Query(description="Filter by movie ID")] = None,
    theater_id: Annotated[
        Optional[int], Query(description="Filter by theater ID")
    ] = None,
    start_time_after: Annotated[
        Optional[datetime], Query(description="Showtimes starting after this time")
    ] = None,
    end_time_before: Annotated[
        Optional[datetime], Query(description="Showtimes ending before this time")
    ] = None,
    is_active: Annotated[
        Optional[bool], Query(description="Filter by active status")
    ] = True,
    offset: Annotated[int, Query(ge=0, description="Pagination offset")] = 0,
    limit: Annotated[
        int, Query(ge=1, le=100, description="Pagination limit (1-100)")
    ] = 10,
    use_case: GetShowtimesUseCase = Depends(get_showtimes_use_case),
) -> List[Showtime]:
    logger.info(
        f"LIST showtimes started | offset:{offset} | limit:{limit} | movie_id:{movie_id} | theater_id:{theater_id} | client:{request.client.host if request.client else None}"
    )
    filters = {}
    try:
        filters: Dict[str, Any] = {
            "movie_id": movie_id,
            "theater_id": theater_id,
            "is_active": is_active,
            "start_time_after": start_time_after,
            "end_time_before": end_time_before,
        }
        filters = {k: v for k, v in filters.items() if v is not None}

        page = PaginationParams(offset=offset, limit=limit)
        showtimes = await use_case.execute(filters=filters, page_params=page)
        logger.info(f"LIST showtimes success | count:{len(showtimes)}")
        return showtimes
    except Exception as e:
        logger.error(f"LIST showtimes failed | error:{str(e)} | filters:{filters}")
        raise


@router.post("/", response_model=Showtime, status_code=status.HTTP_201_CREATED)
async def create_showtime(
    request: Request,
    showtime_data: ShowtimeCreate,
    use_case: ScheduleShowtimeUseCase = Depends(schedule_showtime_use_case),
):
    logger.info(
        f"POST showtime started | movie_id:{showtime_data.movie_id} | theater_id:{showtime_data.theater_id} | client:{request.client.host if request.client else None}"
    )
    try:
        showtime = await use_case.execute(showtime_data)
        logger.info(
            f"POST showtime success | showtime_id:{showtime.id} | movie_id:{showtime.movie_id}"
        )
        return showtime
    except Exception as e:
        logger.error(
            f"POST showtime failed | movie_id:{showtime_data.movie_id} | error:{str(e)}"
        )
        raise


@router.put("/{showtime_id}", response_model=Showtime)
async def update_showtime(
    showtime_id: int,
    request: Request,
    update_data: ShowtimeUpdate,
    use_case: UpdateShowtimeUseCase = Depends(update_showtime_use_case),
):
    logger.info(
        f"PUT showtime started | showtime_id:{showtime_id} | client:{request.client.host if request.client else None}"
    )
    try:
        showtime = await use_case.execute(showtime_id, update_data)
        logger.info(f"PUT showtime success | showtime_id:{showtime_id}")
        return showtime
    except Exception as e:
        logger.error(
            f"PUT showtime failed | showtime_id:{showtime_id} | error:{str(e)}"
        )
        raise


@router.delete("/{showtime_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_showtime(
    request: Request,
    showtime_id: int,
    use_case: DeleteShowtimeUseCase = Depends(delete_showtime_use_case),
):
    logger.info(
        f"DELETE showtime started | showtime_id:{showtime_id} | client:{request.client.host if request.client else None}"
    )
    try:
        await use_case.execute(showtime_id)
        logger.info(f"DELETE showtime success | showtime_id:{showtime_id}")
    except Exception as e:
        logger.error(
            f"DELETE showtime failed | showtime_id:{showtime_id} | error:{str(e)}"
        )
        raise
