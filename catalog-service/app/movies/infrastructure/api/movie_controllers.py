from typing import Annotated
from fastapi import APIRouter, Depends, Query, status, Request
from app.shared.core.pagination import PaginationParams, Page
from app.movies.domain.entities import Movie
from app.movies.application.dtos import (
    MovieDetailResponse,
    PaginatedMovieResponse,
    SearchMovieFilters,
)
from app.movies.application.use_cases import (
    GetMovieByIdUseCase,
    GetMoviesInExhitionUseCase,
    SearchMoviesUseCase,
    UpdateMovieUseCase,
    CreateMovieUseCase,
    DeleteMovieUseCase,
)
from .container import movie_use_cases
from app.shared.core.jwt_security import AuthUserContext, require_roles
from app.config.rate_limit import limiter
import logging

logger = logging.getLogger("app")
router = APIRouter(prefix="/api/v1/movies")


@router.get("/{movie_id}", response_model=MovieDetailResponse)
@limiter.limit("60/minute")
async def get_movie_by_id(
    movie_id: int,
    use_case: Annotated[
        GetMovieByIdUseCase, Depends(movie_use_cases.get_movie_by_id_use_case)
    ],
    request: Request,
):
    movie = await use_case.execute(movie_id)
    return MovieDetailResponse.model_validate(movie.model_dump(mode="json"))


@router.get("/active/", response_model=PaginatedMovieResponse)
@limiter.limit("60/minute")
async def get_movies_in_exhibition(
    use_case: Annotated[
        GetMoviesInExhitionUseCase, Depends(movie_use_cases.get_active_movies_use_case)
    ],
    request: Request,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    params = PaginationParams(offset=offset, limit=limit)
    page: Page[Movie] = await use_case.execute(params)

    logger.info(f"GET active movies success | total:{page.total}")
    return PaginatedMovieResponse.from_page(page)


@router.get("/", response_model=PaginatedMovieResponse)
@limiter.limit("60/minute")
async def search_movies(
    use_case: Annotated[
        SearchMoviesUseCase, Depends(movie_use_cases.search_movies_use_case)
    ],
    filters: Annotated[SearchMovieFilters, Depends()],
    request: Request,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    params = PaginationParams(offset=offset, limit=limit)
    page: Page[Movie] = await use_case.execute(params, filters)

    logger.info(f"GET search movies success | total:{page.total}")
    return PaginatedMovieResponse.from_page(page)


@router.post(
    "/", response_model=MovieDetailResponse, status_code=status.HTTP_201_CREATED
)
@limiter.limit("10/minute")
async def create_movies(
    movie: Movie,
    use_case: Annotated[
        CreateMovieUseCase, Depends(movie_use_cases.create_movie_use_case)
    ],
    current_user: Annotated[
        AuthUserContext, Depends(require_roles("admin", "manager"))
    ],
    request: Request,
):
    created_movie = await use_case.execute(movie)
    return created_movie


@router.put(
    "/{movie_id}", response_model=MovieDetailResponse, status_code=status.HTTP_200_OK
)
@limiter.limit("10/minute")
async def update_movie(
    movie_id: int,
    movie: Movie,
    use_case: Annotated[
        UpdateMovieUseCase, Depends(movie_use_cases.update_movie_use_case)
    ],
    current_user: Annotated[
        AuthUserContext, Depends(require_roles("admin", "manager"))
    ],
    request: Request,
):
    updated_movie = await use_case.execute(movie_id, movie)
    return updated_movie


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/minute")
async def delete_movie(
    movie_id: int,
    use_case: Annotated[
        DeleteMovieUseCase, Depends(movie_use_cases.delete_movie_use_case)
    ],
    current_user: Annotated[
        AuthUserContext, Depends(require_roles("admin", "manager"))
    ],
    request: Request,
):
    await use_case.execute(movie_id)
