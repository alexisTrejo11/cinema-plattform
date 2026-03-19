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
from app.config.jwt_auth_middleware import AuthUserContext, require_roles
from app.config.rate_limit import limiter

router = APIRouter(prefix="/api/v1/theaters", tags=["theaters"])


@router.get("/{theater_id}", response_model=Theater)
@limiter.limit("60/minute")
async def get_theater(
    theater_id: int,
    request: Request,
    use_case: GetTheaterByIdUseCase = Depends(get_theater_by_id_use_case),
):
    return await use_case.execute(theater_id)


@router.get("/", response_model=List[Theater])
@limiter.limit("60/minute")
async def list_theaters(
    request: Request,
    page: int = 1,
    limit: int = 10,
    use_case: ListTheatersUseCase = Depends(list_theaters_use_case),
):
    page_params = {"offset": (page - 1) * limit, "limit": limit}
    return await use_case.execute(page_params=page_params)


@router.get("/cinema/{cinema_id}", response_model=List[Theater])
@limiter.limit("60/minute")
async def get_theaters_by_cinema(
    cinema_id: int,
    request: Request,
    use_case: GetTheatersByCinemaUseCase = Depends(get_theaters_by_cinema_use_case),
):
    return await use_case.execute(cinema_id)


@router.post("/", response_model=Theater, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def create_theater(
    new_theater: Theater,
    request: Request,
    use_case: CreateTheaterUseCase = Depends(create_theater_use_case),
    current_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    return await use_case.execute(new_theater)


@router.put("/{theater_id}", response_model=Theater)
@limiter.limit("10/minute")
async def update_theater(
    theater_id: int,
    update_theater: Theater,
    request: Request,
    use_case: UpdateTheaterUseCase = Depends(update_theater_use_case),
    current_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    return await use_case.execute(theater_id, update_theater)


@router.delete("/{theater_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/minute")
async def delete_theater(
    theater_id: int,
    request: Request,
    use_case: DeleteTheaterUseCase = Depends(delete_theater_use_case),
    current_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    return await use_case.execute(theater_id)
