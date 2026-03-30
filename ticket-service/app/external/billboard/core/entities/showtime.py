from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..enums.showtime_enum import ShowtimeLanguage, ShowtimeType
from .cinema import Cinema
from .movie import Movie
from .theater import Theater


class Showtime(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    id: int = Field(gt=0)
    movie: Movie
    cinema: Cinema
    theater: Theater
    price: Decimal = Field(gt=0)
    start_time: datetime
    type: ShowtimeType
    language: ShowtimeLanguage
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    @field_validator('price')
    @classmethod
    def validate_price_precision(cls, value: Decimal) -> Decimal:
        exponent = value.as_tuple().exponent
        if isinstance(exponent, int) and exponent < -2:
            raise ValueError('Price can have at most 2 decimal places.')
        return value

    def get_id(self) -> int:
        return self.id

    def get_movie(self) -> Movie:
        return self.movie

    def get_movie_id(self) -> Optional[int]:
        return self.movie.get_id()

    def get_cinema(self) -> Cinema:
        return self.cinema

    def get_theater(self) -> Theater:
        return self.theater

    def get_theater_id(self) -> int:
        return self.theater.theater_id

    def get_price(self) -> Decimal:
        return self.price

    def get_start_time(self) -> datetime:
        return self.start_time

    def get_type(self) -> ShowtimeType:
        return self.type

    def get_language(self) -> ShowtimeLanguage:
        return self.language

    def get_created_at(self) -> datetime:
        return self.created_at

    def get_updated_at(self) -> Optional[datetime]:
        return self.updated_at

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(mode='json')
