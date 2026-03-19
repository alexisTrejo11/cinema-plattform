from pydantic import Field, BaseModel, field_validator
from typing import Optional
from datetime import datetime
from decimal import Decimal
from ..enums import ShowtimeLanguage, ShowtimeType, ShowtimeStatus


class ShowtimeBase(BaseModel):
    """Base schema for common Showtime attributes."""

    movie_id: int
    cinema_id: int
    theater_id: int
    price: Decimal = Field(..., max_digits=6, decimal_places=2)
    start_time: datetime
    end_time: datetime
    type: ShowtimeType
    language: ShowtimeLanguage
    status: ShowtimeStatus

    @field_validator("start_time")
    @classmethod
    def validate_start_time_timezone(cls, v):
        if v.tzinfo is None:
            raise ValueError("start_time must include time zone information")
        return v

    @field_validator("end_time")
    @classmethod
    def validate_end_time_timezone(cls, v):
        if v is not None and v.tzinfo is None:
            raise ValueError("end_time must include time zone information")
        return v


class ShowtimeSeatBase(BaseModel):
    """
    Base schema for ShowtimeSeat, containing common attributes.
    """

    showtime_id: int = Field(
        ..., description="The ID of the showtime this seat belongs to."
    )
    theater_seat_id: int = Field(
        ..., description="The ID of the specific theater seat."
    )
    taken_at: Optional[datetime] = Field(
        None, description="Timestamp when the seat was taken/booked."
    )
    user_id: Optional[int] = Field(
        None, description="The ID of the user who took this seat."
    )
