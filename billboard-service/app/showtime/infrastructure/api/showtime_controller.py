from typing import Annotated, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, Query, status, Request

from app.shared.core.pagination import PaginationParams, Page
from app.showtime.domain.entities import Showtime
from app.showtime.application.dtos import (
    ShowtimeCreate,
    ShowtimeUpdate,
    ShowtimeDetailResponse,
    PaginatedShowtimeResponse,
    SearchShowtimeFilters,
)
from app.showtime.application.use_cases import (
    GetShowtimeByIdUseCase,
    SearchShowtimesUseCase,
    DraftShowtimeUseCase,
    LaunchShowtimeUseCase,
    CancelShowtimeUseCase,
    RestoreShowtimeUseCase,
    UpdateShowtimeUseCase,
    DeleteShowtimeUseCase,
)
from app.shared.core.jwt_security import AuthUserContext, require_roles
from app.config.rate_limit import limiter
from .showtime_use_case_container import showtime_use_cases


router = APIRouter(prefix="/api/v1/showtimes", tags=["showtimes"])


@router.get("/{showtime_id}", response_model=ShowtimeDetailResponse)
@limiter.limit("60/minute")
async def get_showtime(
    request: Request,
    showtime_id: int,
    use_case: GetShowtimeByIdUseCase = Depends(
        showtime_use_cases.get_showtime_by_id_use_case
    ),
):
    showtime = await use_case.execute(showtime_id)
    return ShowtimeDetailResponse.model_validate(showtime)


@router.get("/", response_model=PaginatedShowtimeResponse)
@limiter.limit("60/minute")
async def search_showtimes(
    request: Request,
    filters: Annotated[SearchShowtimeFilters, Depends()],
    offset: Annotated[int, Query(ge=0, description="Pagination offset")] = 0,
    limit: Annotated[
        int, Query(ge=1, le=100, description="Pagination limit (1-100)")
    ] = 10,
    use_case: SearchShowtimesUseCase = Depends(
        showtime_use_cases.search_showtimes_use_case
    ),
) -> PaginatedShowtimeResponse:
    params = PaginationParams(offset=offset, limit=limit)
    page: Page[Showtime] = await use_case.execute(params, filters)
    return PaginatedShowtimeResponse.from_page(page)


@router.post("/", response_model=Showtime, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def draft_showtime(
    request: Request,
    showtime_data: ShowtimeCreate,
    use_case: DraftShowtimeUseCase = Depends(
        showtime_use_cases.draft_showtime_use_case
    ),
    current_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    return await use_case.execute(showtime_data)


@router.post("/{showtime_id}/launch", response_model=ShowtimeDetailResponse)
@limiter.limit("10/minute")
async def launch_showtime(
    showtime_id: int,
    request: Request,
    use_case: LaunchShowtimeUseCase = Depends(
        showtime_use_cases.launch_showtime_use_case
    ),
    current_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    showtime = await use_case.execute(showtime_id)
    return ShowtimeDetailResponse.model_validate(showtime)


@router.post("/{showtime_id}/cancel", response_model=ShowtimeDetailResponse)
@limiter.limit("10/minute")
async def cancel_showtime(
    showtime_id: int,
    request: Request,
    use_case: CancelShowtimeUseCase = Depends(
        showtime_use_cases.cancel_showtime_use_case
    ),
    current_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    showtime = await use_case.execute(showtime_id)
    return ShowtimeDetailResponse.model_validate(showtime)


@router.post("/{showtime_id}/restore", response_model=ShowtimeDetailResponse)
@limiter.limit("10/minute")
async def restore_showtime(
    showtime_id: int,
    request: Request,
    use_case: RestoreShowtimeUseCase = Depends(
        showtime_use_cases.restore_showtime_use_case
    ),
    current_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    showtime = await use_case.execute(showtime_id)
    return ShowtimeDetailResponse.model_validate(showtime)


@router.put("/{showtime_id}", response_model=Showtime)
@limiter.limit("10/minute")
async def update_showtime(
    showtime_id: int,
    request: Request,
    update_data: ShowtimeUpdate,
    use_case: UpdateShowtimeUseCase = Depends(
        showtime_use_cases.update_showtime_use_case
    ),
    current_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    return await use_case.execute(showtime_id, update_data)


@router.delete("/{showtime_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/minute")
async def delete_showtime(
    request: Request,
    showtime_id: int,
    use_case: DeleteShowtimeUseCase = Depends(
        showtime_use_cases.delete_showtime_use_case
    ),
    current_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    await use_case.execute(showtime_id)
