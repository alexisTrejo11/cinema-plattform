from token import OP
from pydantic import BaseModel, Field, PositiveInt, HttpUrl
from .enums import MovieGenre, MovieRating
from typing import Optional
from datetime import datetime, date
from pydantic import ConfigDict


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., max_length=200)
    original_title: Optional[str] = None
    minute_duration: PositiveInt = Field(..., description="Duration in minutes")
    release_date: date
    projection_start_date: date
    projection_end_date: date
    synopsis: str
    genre: MovieGenre
    rating: MovieRating
    poster_url: Optional[HttpUrl] = None
    trailer_url: Optional[HttpUrl] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )

    @property
    def is_active(self) -> bool:
        return self.deleted_at is None

    def is_showing(self, on_date: Optional[date] = None) -> bool:
        if on_date is None:
            on_date = date.today()
        return self.projection_start_date <= on_date <= self.projection_end_date
