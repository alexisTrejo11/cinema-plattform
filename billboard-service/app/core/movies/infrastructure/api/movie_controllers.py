from typing import Annotated
from fastapi import APIRouter, Depends, status, Request
from app.core.movies.domain.entities import Movie
from app.core.movies.application.use_cases import (
    GetMovieByIdUseCase,
    GetMoviesInExhitionUseCase,
    UpdateMovieUseCase,
    CreateMovieUseCase,
    DeleteMovieUseCase,
)
from .dependencies import (
    get_movie_by_id_use_case,
    get_active_movies_use_case,
    create_movie_use_case,
    update_movie_use_case,
    delete_movie_use_case,
)
import logging

logger = logging.getLogger("app")
router = APIRouter(prefix="/api/v1/movies")


@router.get("/{movie_id}", response_model=Movie)
async def get_movie_by_id(
    movie_id: int,
    use_case: Annotated[GetMovieByIdUseCase, Depends(get_movie_by_id_use_case)],
    request: Request,
):
    logger.info(
        f"GET movie started | movie_id:{movie_id} | client:{request.client.host if request.client else None}"
    )
    try:
        movie = await use_case.execute(movie_id)
        logger.info(f"GET movie success | movie_id:{movie_id}")
        return movie
    except Exception as e:
        logger.error(f"GET movie failed | movie_id:{movie_id} | error:{str(e)}")
        raise


@router.get("/active/", response_model=list[Movie])
async def get_movies_in_exhibition(
    use_case: Annotated[
        GetMoviesInExhitionUseCase, Depends(get_active_movies_use_case)
    ],
    request: Request,
):
    logger.info(
        f"GET active movies started | client:{request.client.host if request.client else None}"
    )
    try:
        movies = await use_case.execute()
        logger.info(f"GET active movies success | count:{len(movies)}")
        return movies
    except Exception as e:
        logger.error(f"GET active movies failed | error:{str(e)}")
        raise


@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
async def create_movies(
    movie: Movie,
    use_case: Annotated[CreateMovieUseCase, Depends(create_movie_use_case)],
    request: Request,
):
    logger.info(
        f"POST movie started | client:{request.client.host if request.client else None} | title:{movie.title}"
    )
    try:
        created_movie = await use_case.execute(movie)
        logger.info(
            f"POST movie success | movie_id:{created_movie.id} | title:{created_movie.title}"
        )
        return created_movie
    except Exception as e:
        logger.error(f"POST movie failed | title:{movie.title} | error:{str(e)}")
        raise


@router.put("/{movie_id}", response_model=Movie, status_code=status.HTTP_200_OK)
async def update_movie(
    movie_id: int,
    movie: Movie,
    use_case: Annotated[UpdateMovieUseCase, Depends(update_movie_use_case)],
    request: Request,
):
    logger.info(
        f"PUT movie started | movie_id:{movie_id} | client:{request.client.host if request.client else None}"
    )
    try:
        updated_movie = await use_case.execute(movie_id, movie)
        logger.info(
            f"PUT movie success | movie_id:{movie_id} | new_title:{updated_movie.title}"
        )
        return updated_movie
    except Exception as e:
        logger.error(f"PUT movie failed | movie_id:{movie_id} | error:{str(e)}")
        raise


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(
    movie_id: int,
    use_case: Annotated[DeleteMovieUseCase, Depends(delete_movie_use_case)],
    request: Request,
):
    logger.info(
        f"DELETE movie started | movie_id:{movie_id} | client:{request.client.host if request.client else None}"
    )
    try:
        await use_case.execute(movie_id)
        logger.info(f"DELETE movie success | movie_id:{movie_id}")
    except Exception as e:
        logger.error(f"DELETE movie failed | movie_id:{movie_id} | error:{str(e)}")
        raise
