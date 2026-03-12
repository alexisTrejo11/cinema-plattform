from typing import Annotated, List
from fastapi import APIRouter, Depends, Query, status, Request
from app.core.cinema.domain.entities import Cinema
from app.core.cinema.application.dtos import (
    CreateCinemaRequest,
    UpdateCinemaRequest,
)
from app.core.cinema.application.usecases import (
    GetCinemaByIdUseCase,
    ListActiveCinemasUseCase,
    SearchCinemasUseCase,
    CreateCinemaUseCase,
    UpdateCinemaUseCase,
    DeleteCinemaUseCase,
)
from app.core.cinema.application.dtos import SearchCinemaFilters
from .depedencies import (
    get_cinema_by_id_use_case,
    get_active_cinemas_use_case,
    search_cinemas_use_case,
    update_cinema_use_case,
    create_cinema_use_case,
    delete_cinema_use_case,
    get_filters,
)
import logging

logger = logging.getLogger("app")
router = APIRouter(prefix="/api/v1/cinemas")


@router.get("/{cinema_id}", response_model=Cinema)
async def get_cinema_by_id(
    cinema_id: int,
    use_case: Annotated[GetCinemaByIdUseCase, Depends(get_cinema_by_id_use_case)],
    request: Request,
):
    logger.info(
        f"GET cinema started | cinema_id:{cinema_id} | client:{request.client.host if request.client else None}"
    )

    cinema = await use_case.execute(cinema_id)

    logger.info(f"GET cinema success | cinema_id:{cinema_id}")
    return cinema


@router.get("/active/", response_model=list[Cinema])
async def get_active_cinemas(
    use_case: Annotated[ListActiveCinemasUseCase, Depends(get_active_cinemas_use_case)],
    request: Request,
):
    logger.info(
        f"GET active cinemas started | client:{request.client.host if request.client else None}"
    )
    cinemas = await use_case.execute()
    logger.info(f"GET active cinemas success | count:{len(cinemas)}")
    return cinemas


@router.get("/", response_model=List[Cinema])
async def search_cinemas(
    use_case: Annotated[SearchCinemasUseCase, Depends(search_cinemas_use_case)],
    filters: Annotated[SearchCinemaFilters, Depends(get_filters)],
    request: Request,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    logger.info(
        f"SEARCH cinemas started | offset:{offset} | limit:{limit} | filters:{filters.model_dump()} | client:{request.client.host if request.client else None}"
    )
    filter_params = {}
    try:
        page_params = {"offset": offset, "limit": limit}
        filter_params = filters.model_dump(exclude_none=True)
        cinemas = await use_case.execute(page_params, filter_params)
        logger.info(f"SEARCH cinemas success | count:{len(cinemas)}")
        return cinemas
    except Exception as e:
        logger.error(
            f"SEARCH cinemas failed | error:{str(e)} | filters:{filter_params}"
        )
        raise


@router.post("/", response_model=Cinema, status_code=status.HTTP_201_CREATED)
async def create_cinema(
    cinema: CreateCinemaRequest,
    use_case: Annotated[CreateCinemaUseCase, Depends(create_cinema_use_case)],
    request: Request,
):
    logger.info(
        f"POST cinema started | name:{cinema.name} | client:{request.client.host if request.client else None}"
    )
    try:
        created_cinema = await use_case.execute(cinema)
        logger.info(
            f"POST cinema success | cinema_id:{created_cinema.id} | name:{created_cinema.name}"
        )
        return created_cinema
    except Exception as e:
        logger.error(f"POST cinema failed | name:{cinema.name} | error:{str(e)}")
        raise


@router.put("/{cinema_id}", response_model=Cinema)
async def update_cinemas(
    cinema_id: int,
    cinema: UpdateCinemaRequest,
    use_case: Annotated[UpdateCinemaUseCase, Depends(update_cinema_use_case)],
    request: Request,
):
    logger.info(
        f"PUT cinema started | cinema_id:{cinema_id} | client:{request.client.host if request.client else None}"
    )
    try:
        updated_cinema = await use_case.execute(cinema_id, cinema)
        logger.info(
            f"PUT cinema success | cinema_id:{cinema_id} | name:{updated_cinema.name}"
        )
        return updated_cinema
    except Exception as e:
        logger.error(f"PUT cinema failed | cinema_id:{cinema_id} | error:{str(e)}")
        raise


@router.delete("/{cinema_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cinema(
    cinema_id: int,
    use_case: Annotated[DeleteCinemaUseCase, Depends(delete_cinema_use_case)],
    request: Request,
):
    logger.info(
        f"DELETE cinema started | cinema_id:{cinema_id} | client:{request.client.host if request.client else None}"
    )
    try:
        await use_case.execute(cinema_id)
        logger.info(f"DELETE cinema success | cinema_id:{cinema_id}")
    except Exception as e:
        logger.error(f"DELETE cinema failed | cinema_id:{cinema_id} | error:{str(e)}")
        raise
