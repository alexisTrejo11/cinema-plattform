from typing import Any, Optional, List, TYPE_CHECKING
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator, ConfigDict
from app.core.showtime.domain.entities.showtime import ShowtimeBase
from app.core.showtime.domain.enums import (
    ShowtimeLanguage,
    ShowtimeType,
    ShowtimeStatus,
)
from app.core.showtime.domain.entities.showtime_seat import ShowtimeSeatBase
from app.core.shared.pagination import PaginationResponse

if TYPE_CHECKING:
    from app.core.shared.pagination import Page
    from app.core.showtime.domain.entities import Showtime


class SearchShowtimeFilters(BaseModel):
    """Filter parameters for showtime search."""

    movie_id: Optional[int] = None
    theater_id: Optional[int] = None
    cinema_id: Optional[int] = None
    type: Optional[ShowtimeType] = None
    language: Optional[ShowtimeLanguage] = None
    start_time_after: Optional[datetime] = None
    start_time_before: Optional[datetime] = None
    status: Optional[ShowtimeStatus] = None
    is_upcoming: Optional[bool] = None
    min_available_seats: Optional[int] = None


class ShowtimeSummaryResponse(BaseModel):
    """Lightweight showtime response for list/search endpoints."""

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 101,
                    "movie_id": 10,
                    "theater_id": 3,
                    "cinema_id": 1,
                    "price": "10.50",
                    "start_time": "2026-03-19T20:30:00Z",
                    "end_time": "2026-03-19T22:45:00Z",
                    "type": "IMAX_3D",
                    "language": "DUBBED_SPANISH",
                    "available_seats": 48,
                }
            ]
        },
    )

    id: int = Field(
        ..., description="Unique identifier of the showtime.", examples=[101]
    )
    movie_id: int = Field(..., description="ID of the movie.", examples=[10])
    theater_id: int = Field(..., description="ID of the theater.", examples=[3])
    cinema_id: int = Field(..., description="ID of the cinema.", examples=[1])
    price: Decimal = Field(
        ..., description="Ticket price for this showtime.", examples=["10.50"]
    )
    start_time: datetime = Field(
        ...,
        description="Start time of the showtime (ISO-8601).",
        examples=["2026-03-19T20:30:00Z"],
    )
    end_time: datetime = Field(
        ...,
        description="End time of the showtime (ISO-8601).",
        examples=["2026-03-19T22:45:00Z"],
    )
    type: ShowtimeType = Field(
        ..., description="Type of showtime (2D, 3D, IMAX, etc.)."
    )
    language: ShowtimeLanguage = Field(
        ...,
        description="Language of the showtime.",
        examples=[ShowtimeLanguage.DUBBED_SPANISH],
    )
    available_seats: int = Field(
        0, ge=0, description="Number of currently available seats.", examples=[48]
    )


class ShowtimeDetailResponse(BaseModel):
    """Complete showtime response with all details."""

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 101,
                    "movie_id": 10,
                    "theater_id": 3,
                    "cinema_id": 1,
                    "price": "10.50",
                    "start_time": "2026-03-19T20:30:00Z",
                    "end_time": "2026-03-19T22:45:00Z",
                    "status": "UPCOMING",
                    "type": "IMAX_3D",
                    "language": "DUBBED_SPANISH",
                    "total_seats": 200,
                    "available_seats": 48,
                    "created_at": "2026-03-01T10:00:00Z",
                    "updated_at": "2026-03-10T12:00:00Z",
                }
            ]
        },
    )

    id: int
    movie_id: int
    theater_id: int
    cinema_id: int
    price: Decimal
    start_time: datetime
    end_time: datetime
    type: ShowtimeType
    status: ShowtimeStatus
    language: ShowtimeLanguage
    total_seats: int = Field(
        ..., ge=0, description="Total seats assigned to this showtime."
    )
    available_seats: int = Field(..., ge=0, description="Remaining available seats.")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class PaginatedShowtimeResponse(PaginationResponse):
    """Paginated response for showtime list/search endpoints."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "data": [
                        {
                            "id": 101,
                            "movie_id": 10,
                            "theater_id": 3,
                            "cinema_id": 1,
                            "price": "10.50",
                            "start_time": "2026-03-19T20:30:00Z",
                            "end_time": "2026-03-19T22:45:00Z",
                            "type": "IMAX_3D",
                            "language": "DUBBED_SPANISH",
                            "available_seats": 48,
                        }
                    ],
                    "page_size": 10,
                    "total_items": 42,
                    "total_pages": 5,
                    "current_page": 1,
                    "next_page": 2,
                    "previous_page": 1,
                    "has_next": True,
                    "has_previous": False,
                }
            ]
        }
    )

    data: List[ShowtimeSummaryResponse]

    @classmethod
    def from_page(cls, page: "Page[Showtime]") -> "PaginatedShowtimeResponse":
        """
        Convert a Page[Showtime] domain object to PaginatedShowtimeResponse DTO.

        Args:
            page: Page object containing Showtime entities and pagination metadata

        Returns:
            PaginatedShowtimeResponse with converted data
        """
        showtime_summaries = [
            ShowtimeSummaryResponse.model_validate(showtime) for showtime in page.items
        ]

        return cls(
            data=showtime_summaries,
            page_size=page.page_size,
            total_items=page.total,
            total_pages=page.total_pages,
            current_page=page.page,
            next_page=(
                min(page.page + 1, page.total_pages) if page.has_next else page.page
            ),
            previous_page=max(page.page - 1, 1) if page.has_previous else page.page,
            has_next=page.has_next,
            has_previous=page.has_previous,
        )


class ShowtimeCreate(ShowtimeBase):
    """Schema for creating a new Showtime. No ID or timestamps."""

    pass


class ShowtimeUpdate(BaseModel):
    """Schema for updating an existing Showtime. All fields optional for partial updates."""

    id: int = Field(
        ..., description="The ID of the showtime to update."
    )  # Required for update
    movie_id: Optional[int] = None
    theater_id: Optional[int] = None
    price: Optional[Decimal] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    type: Optional[ShowtimeType] = None
    language: Optional[ShowtimeLanguage] = None

    @field_validator("start_time")
    @classmethod
    def validate_start_time_timezone(cls, v: Any):
        if v.tzinfo is None:
            raise ValueError("start_time must include time zone information")
        return v

    @field_validator("end_time")
    @classmethod
    def validate_end_time_timezone(cls, v: Any):
        if v is not None and v.tzinfo is None:
            raise ValueError("end_time must include time zone information")
        return v


class ShowtimeSeatCreate(ShowtimeSeatBase):
    """
    Schema for creating a new ShowtimeSeat.
    'id' and timestamps are not included as they are typically generated by the database.
    """

    pass


class ShowtimeSeatUpdate(BaseModel):
    """
    Schema for updating an existing ShowtimeSeat.
    All fields are optional for partial updates.
    """

    id: int = Field(
        ..., description="The unique identifier of the showtime seat to update."
    )
    showtime_id: Optional[int] = Field(
        None, description="The ID of the showtime this seat belongs to."
    )
    theater_seat_id: Optional[int] = Field(
        None, description="The ID of the specific theater seat."
    )
    taken_at: Optional[datetime] = Field(
        None, description="Timestamp when the seat was taken/booked."
    )
    transaction_id: Optional[int] = Field(
        None, description="The ID of the transaction associated with this booking."
    )
    user_id: Optional[int] = Field(
        None, description="The ID of the user who took this seat."
    )
