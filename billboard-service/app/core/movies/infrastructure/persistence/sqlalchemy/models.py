from __future__ import annotations
from sqlalchemy import String, Integer, Boolean, Date, DateTime, Enum as SQLEnum
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from app.config.base_model import Base
from app.core.movies.domain.enums import MovieRating, MovieGenre
from sqlalchemy.orm import mapped_column, relationship, Mapped
from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from app.core.showtime.infrastructure.persistence.sqlalchemy import ShowtimeModel


class MovieModel(Base):
    __tablename__ = "movies"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    title = mapped_column(String(200), nullable=False)
    original_title = mapped_column(String(200))
    minute_duration = mapped_column(Integer, nullable=False)
    release_date = mapped_column(Date, nullable=False)
    end_date = mapped_column(Date, nullable=False)
    description = mapped_column(String, nullable=False)
    genre = mapped_column(SQLEnum(MovieGenre, name="movie_genre"), nullable=False)
    rating = mapped_column(SQLEnum(MovieRating, name="movie_rating"), nullable=False)
    poster_url = mapped_column(String)
    trailer_url = mapped_column(String)
    is_active = mapped_column(Boolean, default=True)
    created_at = mapped_column(DateTime, server_default=func.now())
    updated_at = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    showtimes: Mapped[List["ShowtimeModel"]] = relationship(
        "ShowtimeModel",
        back_populates="movie",
        lazy="select",
        cascade="all, delete-orphan",
    )

    @staticmethod
    def from_domain(entity) -> MovieModel:
        return MovieModel(
            id=entity.id,
            title=entity.title,
            original_title=entity.original_title,
            minute_duration=entity.minute_duration,
            release_date=entity.release_date,
            end_date=entity.end_date,
            description=entity.description,
            genre=entity.genre,
            rating=entity.rating,
            poster_url=str(entity.poster_url) if entity.poster_url else None,
            trailer_url=str(entity.trailer_url) if entity.trailer_url else None,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
