from datetime import date

from pydantic import HttpUrl
from tests.conftest import *
from app.movies.domain.entities import Movie
from app.movies.domain.enums import MovieGenre, MovieRating
from app.movies.infrastructure.persistence.sql_alchemist_repository import SQLAlchemyMovieRepository as MovieRepository


@pytest.fixture
def sample_movie():
    return Movie(
        title="Inception",
        original_title="Inception",
        minute_duration=148,
        release_date=date(2010, 7, 16),
        end_date=date(2010, 12, 31),
        description="A thief who steals corporate secrets through dream-sharing technology",
        genre=MovieGenre.SCI_FI,
        rating=MovieRating.PG_13,
        poster_url=HttpUrl("https://example.com/poster.jpg"),    
        trailer_url=HttpUrl("https://example.com/trailer.mp4"),    
        is_active=True
    )

@pytest.fixture
def inactive_movie():
    return Movie(
        title="Old Movie",
        original_title="Old Movie",
        minute_duration=120,
        release_date=date(2000, 1, 1),
        end_date=date(2000, 12, 31),
        description="An old inactive movie",
        genre=MovieGenre.DRAMA,
        rating=MovieRating.R,
        is_active=False
    )