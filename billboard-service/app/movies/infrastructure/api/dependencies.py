from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.postgres_config import get_db
from app.showtime.infrastructure.persistence.sqlalch_show_repository import SQLAlchemyShowtimeRepository
from ..persistence.sql_alchemist_repository import SQLAlchemyMovieRepository
from ...application.use_cases import GetMovieByIdUseCase, GetMoviesInExhitionUseCase, CreateMovieUseCase, UpdateMovieUseCase, DeleteMovieUseCase, GetMovieShowtimesUseCase

async def get_movie_by_id_use_case(db: AsyncSession = Depends(get_db)) -> GetMovieByIdUseCase:
    repo = SQLAlchemyMovieRepository(db)
    return GetMovieByIdUseCase(repo)

async def get_active_movies_use_case(db: AsyncSession = Depends(get_db)) -> GetMoviesInExhitionUseCase:
    repo = SQLAlchemyMovieRepository(db)
    return GetMoviesInExhitionUseCase(repo)

async def create_movie_use_case(db: AsyncSession = Depends(get_db)) -> CreateMovieUseCase:
    repo = SQLAlchemyMovieRepository(db)
    return CreateMovieUseCase(repo)

async def update_movie_use_case(db: AsyncSession = Depends(get_db)) -> UpdateMovieUseCase:
    repo = SQLAlchemyMovieRepository(db)
    return UpdateMovieUseCase(repo)

async def delete_movie_use_case(db: AsyncSession = Depends(get_db)) -> DeleteMovieUseCase:
    repo = SQLAlchemyMovieRepository(db)
    return DeleteMovieUseCase(repo)

async def get_movie_showtimes(db: AsyncSession = Depends(get_db)) -> GetMovieShowtimesUseCase:
    movie_repo = SQLAlchemyMovieRepository(db)
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    return GetMovieShowtimesUseCase(showtime_repo, movie_repo)