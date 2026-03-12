from fastapi import APIRouter, Depends, status, Request
from typing import List
from app.core.theater.application.theather_use_cases import (
    GetTheaterByIdUseCase,
    ListTheatersUseCase,
    CreateTheaterUseCase,
    UpdateTheaterUseCase,
    DeleteTheaterUseCase,
    GetTheatersByCinemaUseCase,
)
from app.core.theater.domain.theater import Theater
from .depdencies import (
    get_theater_by_id_use_case,
    list_theaters_use_case,
    create_theater_use_case,
    update_theater_use_case,
    delete_theater_use_case,
    get_theaters_by_cinema_use_case,
)
import logging

logger = logging.getLogger("app")
router = APIRouter(prefix="/api/v1/theaters", tags=["theaters"])


@router.get("/{theater_id}", response_model=Theater)
async def get_theater(
    theater_id: int,
    request: Request,
    use_case: GetTheaterByIdUseCase = Depends(get_theater_by_id_use_case),
):
    logger.info(
        f"GET theater started | theater_id:{theater_id} | client:{request.client.host if request.client else None}"
    )
    try:
        theater = await use_case.execute(theater_id)
        logger.info(f"GET theater success | theater_id:{theater_id}")
        return theater
    except Exception as e:
        logger.error(f"GET theater failed | theater_id:{theater_id} | error:{str(e)}")
        raise


@router.get("/", response_model=List[Theater])
async def list_theaters(
    request: Request,
    page: int = 1,
    limit: int = 10,
    use_case: ListTheatersUseCase = Depends(list_theaters_use_case),
):
    logger.info(
        f"LIST theaters started | page:{page} | limit:{limit} | client:{request.client.host if request.client else None}"
    )
    try:
        page_params = {"offset": (page - 1) * limit, "limit": limit}
        theaters = await use_case.execute(page_params=page_params)
        logger.info(f"LIST theaters success | count:{len(theaters)}")
        return theaters
    except Exception as e:
        logger.error(
            f"LIST theaters failed | page:{page} | limit:{limit} | error:{str(e)}"
        )
        raise


@router.get("/cinema/{cinema_id}", response_model=List[Theater])
async def get_theaters_by_cinema(
    cinema_id: int,
    request: Request,
    use_case: GetTheatersByCinemaUseCase = Depends(get_theaters_by_cinema_use_case),
):
    logger.info(
        f"GET theaters by cinema started | cinema_id:{cinema_id} | client:{request.client.host if request.client else None}"
    )
    try:
        theaters = await use_case.execute(cinema_id)
        logger.info(
            f"GET theaters by cinema success | cinema_id:{cinema_id} | count:{len(theaters)}"
        )
        return theaters
    except Exception as e:
        logger.error(
            f"GET theaters by cinema failed | cinema_id:{cinema_id} | error:{str(e)}"
        )
        raise


@router.post("/", response_model=Theater, status_code=status.HTTP_201_CREATED)
async def create_theater(
    new_theater: Theater,
    request: Request,
    use_case: CreateTheaterUseCase = Depends(create_theater_use_case),
):
    logger.info(
        f"POST theater started | name:{new_theater.name} | client:{request.client.host if request.client else None}"
    )
    try:
        theater = await use_case.execute(new_theater)
        logger.info(
            f"POST theater success | theater_id:{theater.id} | name:{theater.name}"
        )
        return theater
    except Exception as e:
        logger.error(f"POST theater failed | name:{new_theater.name} | error:{str(e)}")
        raise


@router.put("/{theater_id}", response_model=Theater)
async def update_theater(
    theater_id: int,
    update_theater: Theater,
    request: Request,
    use_case: UpdateTheaterUseCase = Depends(update_theater_use_case),
):
    logger.info(
        f"PUT theater started | theater_id:{theater_id} | client:{request.client.host if request.client else None}"
    )
    try:
        theater = await use_case.execute(theater_id, update_theater)
        logger.info(
            f"PUT theater success | theater_id:{theater_id} | name:{theater.name}"
        )
        return theater
    except Exception as e:
        logger.error(f"PUT theater failed | theater_id:{theater_id} | error:{str(e)}")
        raise


@router.delete("/{theater_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_theater(
    theater_id: int,
    request: Request,
    use_case: DeleteTheaterUseCase = Depends(delete_theater_use_case),
):
    logger.info(
        f"DELETE theater started | theater_id:{theater_id} | client:{request.client.host if request.client else None}"
    )
    try:
        await use_case.execute(theater_id)
        logger.info(f"DELETE theater success | theater_id:{theater_id}")
    except Exception as e:
        logger.error(
            f"DELETE theater failed | theater_id:{theater_id} | error:{str(e)}"
        )
        raise
