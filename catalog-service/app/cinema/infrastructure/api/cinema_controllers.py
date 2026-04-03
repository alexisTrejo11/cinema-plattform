from typing import Annotated, List
from fastapi import APIRouter, Depends, Query, status, Request
from app.shared.core.pagination import PaginationParams, Page
from app.cinema.domain.entities import Cinema
from app.cinema.application.dtos import (
    CreateCinemaRequest,
    UpdateCinemaRequest,
    CinemaResponse,
    PaginatedCinemaSummaryResponse,
    SearchCinemaFilters,
)
from app.cinema.application.usecases import (
    GetCinemaByIdUseCase,
    ListActiveCinemasUseCase,
    SearchCinemasUseCase,
    CreateCinemaUseCase,
    UpdateCinemaUseCase,
    DeleteCinemaUseCase,
    RestoreCinemaUseCase,
)
from app.cinema.application.dtos import SearchCinemaFilters
from .container import cinema_use_cases
from app.shared.core.jwt_security import AuthUserContext, require_roles
from app.config.rate_limit import limiter
import logging

logger = logging.getLogger("app")
router = APIRouter(prefix="/api/v1/cinemas")


@router.get("/{cinema_id}", response_model=CinemaResponse)
@limiter.limit("60/minute")
async def get_cinema_by_id(
    cinema_id: int,
    use_case: Annotated[
        GetCinemaByIdUseCase, Depends(cinema_use_cases.get_cinema_by_id_use_case)
    ],
    request: Request,
):
    """
    Get a cinema by its ID.

    Args:
        cinema_id: The ID of the cinema to get.
        use_case: The use case to get the cinema.
        request: The request object.

    Returns:
        The cinema response JSON.
    Raises:
        ValidationError: If the cinema request is invalid.
        TooManyRequests: If the request is throttled.
        CinemaNotFound: If the cinema is not found.
        InternalServerError: If an internal server error occurs.
    """
    cinema = await use_case.execute(cinema_id)
    return CinemaResponse.model_validate(cinema)


@router.get("/active/", response_model=PaginatedCinemaSummaryResponse)
@limiter.limit("60/minute")
async def get_active_cinemas(
    use_case: Annotated[
        ListActiveCinemasUseCase, Depends(cinema_use_cases.get_active_cinemas_use_case)
    ],
    request: Request,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    params = PaginationParams(offset=offset, limit=limit)
    page: Page[Cinema] = await use_case.execute(params)
    return PaginatedCinemaSummaryResponse.from_page(page)


@router.get("/", response_model=PaginatedCinemaSummaryResponse)
@limiter.limit("60/minute")
async def search_cinemas(
    use_case: Annotated[
        SearchCinemasUseCase, Depends(cinema_use_cases.search_cinemas_use_case)
    ],
    filters: Annotated[SearchCinemaFilters, Depends(cinema_use_cases.get_filters)],
    request: Request,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    params = PaginationParams(offset=offset, limit=limit)
    page: Page[Cinema] = await use_case.execute(params, filters)
    return PaginatedCinemaSummaryResponse.from_page(page)


@router.post("/", response_model=CinemaResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def create_cinema(
    cinema: CreateCinemaRequest,
    use_case: Annotated[
        CreateCinemaUseCase, Depends(cinema_use_cases.create_cinema_use_case)
    ],
    current_user: Annotated[
        AuthUserContext, Depends(require_roles("admin", "manager"))
    ],
    request: Request,
):
    created_cinema = await use_case.execute(cinema)
    return CinemaResponse.model_validate(created_cinema)


@router.put("/{cinema_id}", response_model=CinemaResponse)
@limiter.limit("10/minute")
async def update_cinemas(
    cinema_id: int,
    cinema: UpdateCinemaRequest,
    use_case: Annotated[
        UpdateCinemaUseCase, Depends(cinema_use_cases.update_cinema_use_case)
    ],
    current_user: Annotated[
        AuthUserContext, Depends(require_roles("admin", "manager"))
    ],
    request: Request,
):
    updated_cinema = await use_case.execute(cinema_id, cinema)
    return CinemaResponse.model_validate(updated_cinema)


@router.post("/{cinema_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/minute")
async def restore_cinema(
    cinema_id: int,
    use_case: Annotated[
        RestoreCinemaUseCase, Depends(cinema_use_cases.restore_cinema_use_case)
    ],
    current_user: Annotated[
        AuthUserContext, Depends(require_roles("admin", "manager"))
    ],
    request: Request,
):
    await use_case.execute(cinema_id)
    return None


@router.delete("/{cinema_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/minute")
async def delete_cinema(
    cinema_id: int,
    use_case: Annotated[
        DeleteCinemaUseCase, Depends(cinema_use_cases.delete_cinema_use_case)
    ],
    current_user: Annotated[
        AuthUserContext, Depends(require_roles("admin", "manager"))
    ],
    request: Request,
):
    await use_case.execute(cinema_id)
