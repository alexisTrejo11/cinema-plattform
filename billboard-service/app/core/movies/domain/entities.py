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
    end_date: date
    description: str
    genre: MovieGenre
    rating: MovieRating
    poster_url: Optional[HttpUrl] = None
    trailer_url: Optional[HttpUrl] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )
