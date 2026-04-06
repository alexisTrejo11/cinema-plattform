"""Import ORM models so Base.metadata is complete for Alembic and startup checks."""

from app.cinema.infrastructure.persistence.sqlalchemy import CinemaModel
from app.movies.infrastructure.persistence.sqlalchemy import MovieModel
from app.theater.infrastructure.persistence.sqlalchemy import TheaterModel, TheaterSeatModel

__all__ = ["CinemaModel", "MovieModel", "TheaterModel", "TheaterSeatModel"]
