"""Import ORM models so Base.metadata is complete for Alembic and startup checks."""

from app.movies.infrastructure.persistence.sqlalchemy import MovieModel
from app.showtime.infrastructure.persistence.sqlalchemy import ShowtimeModel
from app.theater.infrastructure.persistence.sqlalchemy import TheaterModel
from app.cinema.infrastructure.persistence.sqlalchemy import CinemaModel

__all__ = ["MovieModel", "ShowtimeModel", "TheaterModel", "CinemaModel"]
