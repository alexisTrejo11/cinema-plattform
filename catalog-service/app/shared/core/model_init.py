"""Import ORM models so Base.metadata is complete for Alembic and startup checks."""

from app.showtime.infrastructure.persistence.sqlalchemy import ShowtimeModel

__all__ = ["ShowtimeModel"]
