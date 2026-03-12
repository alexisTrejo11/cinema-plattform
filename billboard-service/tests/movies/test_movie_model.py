import pytest
from datetime import date, datetime
from app.core.movies.domain.enums import MovieGenre, MovieRating
from app.config.base_model import Base
from app.core.movies.infrastructure.persistence.models import MovieModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="module")
def db_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


def test_movie_model_creation(db_session):
    movie = MovieModel(
        title="Inception",
        original_title="Inception",
        minute_duration=148,
        release_date=date(2010, 7, 16),
        end_date=date(2010, 9, 16),
        description="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        genre=MovieGenre.ACTION,
        rating=MovieRating.PG_13,
        poster_url="https://example.com/inception_poster.jpg",
        trailer_url="https://example.com/inception_trailer.mp4",
        is_active=True,
    )
    db_session.add(movie)
    db_session.commit()
    db_session.refresh(movie)

    assert movie.title == "Inception"
    assert movie.original_title == "Inception"
    assert movie.minute_duration == 148
    assert movie.release_date == date(2010, 7, 16)
    assert movie.end_date == date(2010, 9, 16)
    assert movie.genre == MovieGenre.ACTION
    assert movie.rating == MovieRating.PG_13
    assert movie.poster_url == "https://example.com/inception_poster.jpg"
    assert movie.trailer_url == "https://example.com/inception_trailer.mp4"
    assert movie.is_active is True
    assert isinstance(movie.created_at, datetime)
    assert isinstance(movie.updated_at, datetime)

    assert isinstance(movie.showtimes, list)
