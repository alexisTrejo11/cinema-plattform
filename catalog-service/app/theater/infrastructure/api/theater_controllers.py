from fastapi import APIRouter, Depends, status, Request, Query
from typing import Annotated
from app.shared.core.pagination import PaginationParams, Page
from app.theater.application.use_cases import (
    GetTheaterByIdUseCase,
    ListTheatersUseCase,
    SearchTheatersUseCase,
    CreateTheaterUseCase,
    UpdateTheaterUseCase,
    DeleteTheaterUseCase,
    RestoreTheaterUseCase,
    GetTheatersByCinemaUseCase,
)
from app.theater.application.dtos import (
    SearchTheaterFilters,
    TheaterDetailResponse,
    PaginatedTheaterResponse,
)
from app.theater.domain.theater import Theater
from .theater_use_case_container import theater_use_cases
from app.shared.core.jwt_security import AuthUserContext, require_roles
from app.config.rate_limit import limiter

router = APIRouter(prefix="/api/v1/theaters", tags=["theaters"])


@router.get("/{theater_id}", response_model=TheaterDetailResponse)
@limiter.limit("60/minute")
async def get_theater(
    theater_id: int,
    request: Request,
    use_case: GetTheaterByIdUseCase = Depends(
        theater_use_cases.get_theater_by_id_use_case
    ),
):
    theater = await use_case.execute(theater_id)
    return TheaterDetailResponse.model_validate(theater)


@router.get("/", response_model=PaginatedTheaterResponse)
@limiter.limit("60/minute")
async def search_theaters(
    request: Request,
    filters: Annotated[SearchTheaterFilters, Depends()],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    use_case: SearchTheatersUseCase = Depends(
        theater_use_cases.search_theaters_use_case
    ),
):
    params = PaginationParams(offset=offset, limit=limit)
    page: Page[Theater] = await use_case.execute(params=params, filters=filters)
    return PaginatedTheaterResponse.from_page(page)


@router.get("/cinema/{cinema_id}", response_model=PaginatedTheaterResponse)
@limiter.limit("60/minute")
async def get_theaters_by_cinema(
    cinema_id: int,
    request: Request,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    use_case: GetTheatersByCinemaUseCase = Depends(
        theater_use_cases.get_theaters_by_cinema_use_case
    ),
):
    rows = await use_case.execute(cinema_id)
    sliced = rows[offset : offset + limit]
    total = len(rows)
    page = Page.create(
        items=sliced, total=total, params=PaginationParams(offset=offset, limit=limit)
    )
    return PaginatedTheaterResponse.from_page(page)


@router.post(
    "/", response_model=TheaterDetailResponse, status_code=status.HTTP_201_CREATED
)
@limiter.limit("10/minute")
async def create_theater(
    new_theater: Theater,
    request: Request,
    use_case: CreateTheaterUseCase = Depends(theater_use_cases.create_theater_use_case),
    current_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    created = await use_case.execute(new_theater)
    return TheaterDetailResponse.model_validate(created)


@router.put("/{theater_id}", response_model=TheaterDetailResponse)
@limiter.limit("10/minute")
async def update_theater(
    theater_id: int,
    update_data: Theater,
    request: Request,
    use_case: UpdateTheaterUseCase = Depends(theater_use_cases.update_theater_use_case),
    current_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    updated = await use_case.execute(theater_id, update_data)
    return TheaterDetailResponse.model_validate(updated)


@router.delete("/{theater_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/minute")
async def delete_theater(
    theater_id: int,
    request: Request,
    use_case: DeleteTheaterUseCase = Depends(theater_use_cases.delete_theater_use_case),
    current_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    await use_case.execute(theater_id)
    return None


@router.post("/{theater_id}/restore", response_model=TheaterDetailResponse)
@limiter.limit("10/minute")
async def restore_theater(
    theater_id: int,
    request: Request,
    use_case: RestoreTheaterUseCase = Depends(
        theater_use_cases.restore_theater_use_case
    ),
    current_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    restored = await use_case.execute(theater_id)
    return TheaterDetailResponse.model_validate(restored)
