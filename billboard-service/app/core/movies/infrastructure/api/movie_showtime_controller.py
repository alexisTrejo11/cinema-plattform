from fastapi import APIRouter, Depends, Query, Request
from typing import Annotated, List, Optional
from app.core.shared.pagination import PaginationParams
from app.core.movies.application.dtos import (
    MovieShowtimesFilters,
    MovieShowtime,
    MovieShowtimeResponse,
)
from app.config.rate_limit import limiter
from app.core.movies.infrastructure.api.movie_use_case_container import movie_use_cases
from app.core.movies.application.use_cases import GetMovieShowtimesUseCase

router = APIRouter(prefix="/api/v1/movies/showtimes", tags=["showtimes"])


@router.get(
    "/schedule-details",
    response_model=List[MovieShowtime],
    summary="Get Movie Showtimes",
    description="""Retrieves movie showtimes grouped by movie.
    Allows filtering by cinema, movie, and paginating results.""",
    responses={
        200: {"description": "List of movies with their showtimes"},
        400: {"description": "Invalid parameters"},
        500: {"description": "Internal server error"},
    },
)
@limiter.limit("60/minute")
async def get_movie_showtime(
    request: Request,
    use_case: Annotated[
        GetMovieShowtimesUseCase, Depends(movie_use_cases.get_movie_showtimes)
    ],
    cinema_id_list: Annotated[Optional[List[int]], Query()] = None,
    movie_id: Annotated[Optional[int], Query(ge=1)] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    """
    Endpoint to retrieve available movie showtimes.

    Parameters:
    - cinema_id_list: List of cinema IDs for filtering (optional)
    - movie_id: Specific movie ID (optional)
    - offset: Number of results to skip (for pagination)
    - limit: Maximum number of results per page (1-100)
    """
    page_params = PaginationParams(offset=offset, limit=limit)
    filters = MovieShowtimesFilters(
        cinema_id_list=cinema_id_list,
        movie_id=movie_id,
        incoming=False,  # Incoming False to use demo data
    )

    movie_showtimes = await use_case.execute(filters, page_params)
    return [
        MovieShowtimeResponse.model_validate(movie_showtime.model_dump(mode="json"))
        for movie_showtime in movie_showtimes
    ]
