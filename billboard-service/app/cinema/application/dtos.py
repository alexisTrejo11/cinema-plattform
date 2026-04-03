from datetime import date, datetime
from typing import Optional, List, Any, TYPE_CHECKING
from pydantic import BaseModel, Field, field_validator, ConfigDict

if TYPE_CHECKING:
    from app.shared.pagination import Page
    from app.cinema.domain.entities import Cinema
from app.cinema.domain.enums import (
    CinemaType,
    CinemaStatus,
    CinemaFeatures,
    LocationRegion,
)
from app.cinema.domain.value_objects import (
    CinemaAmenities,
    ContactInfo,
    Location,
    SocialMedia,
)
from app.cinema.domain.base import CinemaBase
from app.shared.core.pagination import PaginationMetadata


class CreateCinemaRequest(CinemaBase):
    """Model for creating new cinemas (all fields required except ID)"""

    pass


class UpdateCinemaRequest(BaseModel):
    """Model for partial updates with all optional fields"""

    model_config = ConfigDict(
        extra="forbid", json_encoders={date: lambda v: v.isoformat()}
    )

    image: Optional[str] = Field(
        None, description="URL or path to the cinema's main image."
    )
    name: Optional[str] = Field(
        None, max_length=255, min_length=3, description="Name of the cinema."
    )
    tax_number: Optional[str] = Field(
        None, max_length=255, min_length=5, description="Tax ID number."
    )
    is_active: Optional[bool] = Field(None, description="Operational status flag.")
    description: Optional[str] = Field(None, description="Brief description.")
    screens: Optional[int] = Field(None, ge=0, description="Number of screens.")
    last_renovation: Optional[date] = Field(None, description="Last renovation date.")

    type: Optional[CinemaType] = Field(None, description="Type of cinema.")
    status: Optional[CinemaStatus] = Field(None, description="Operational status.")
    amenities: Optional[CinemaAmenities] = Field(None, description="Amenities details.")
    region: Optional[LocationRegion] = Field(None, description="Region location.")

    contact_info: Optional[ContactInfo] = Field(
        None, description="Contact information."
    )
    location: Optional[Location] = Field(None, description="Geographical coordinates.")
    social_media: Optional[SocialMedia] = Field(None, description="Social media links.")
    features: Optional[List[CinemaFeatures]] = Field(
        None, description="Special features."
    )

    @field_validator("last_renovation")
    @classmethod
    def validate_last_renovation_not_future(cls, v: Optional[date]) -> Optional[date]:
        if v is not None and v > date.today():
            raise ValueError("Last renovation date cannot be in the future.")
        return v

    def dict(self, exclude_none=True, **kwargs) -> dict[str, Any]:
        """Override dict to exclude None values by default for partial updates"""
        return super().model_dump(exclude_none=exclude_none, **kwargs)


class SearchCinemaFilters(BaseModel):
    """Model for search filters with all optional fields"""

    name: Optional[str] = None
    tax_number: Optional[str] = None
    is_active: Optional[bool] = None
    min_screens: Optional[int] = None
    max_screens: Optional[int] = None
    type: Optional[CinemaType] = None
    status: Optional[CinemaStatus] = None
    region: Optional[LocationRegion] = None
    has_parking: Optional[bool] = None
    has_food_court: Optional[bool] = None
    renovated_after: Optional[date] = None
    renovated_before: Optional[date] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    email_contact: Optional[str] = None


class CinemaSummaryResponse(BaseModel):
    """
    Lightweight cinema response for list/search endpoints.

    Includes only the most useful fields while keeping the payload small.
    """

    id: int = Field(..., description="Unique identifier of the cinema.", examples=[12])
    name: str = Field(
        ...,
        max_length=255,
        min_length=3,
        description="Cinema name.",
        examples=["Cinepolis Centro"],
    )
    image: str = Field(
        "",
        description="URL or path to the cinema's main image.",
        examples=["https://cdn.example.com/cinemas/12.jpg"],
    )
    type: CinemaType = Field(
        ...,
        description="Cinema type (e.g., VIP, Traditional).",
        examples=[CinemaType.VIP],
    )
    status: CinemaStatus = Field(
        ...,
        description="Current operational status.",
        examples=[CinemaStatus.OPEN],
    )
    is_active: bool = Field(
        False,
        description="Whether the cinema is operational/active.",
        examples=[True],
    )
    screens: int = Field(
        ...,
        ge=0,
        description="Number of screens in the cinema.",
        examples=[8],
    )
    last_renovation: Optional[date] = Field(
        None,
        description="Date of the last major renovation (if available).",
        examples=["2024-08-15"],
    )
    region: LocationRegion = Field(
        ...,
        description="Geographical region where the cinema is located.",
        examples=[LocationRegion.CDMX_CENTER],
    )
    amenities: CinemaAmenities = Field(
        ...,
        description="Amenities available at the cinema (e.g., parking, food court).",
    )

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_encoders={date: lambda v: v.isoformat()},
        extra="forbid",
        json_schema_extra={
            "examples": [
                {
                    "id": 12,
                    "name": "Cinepolis Centro",
                    "image": "https://cdn.example.com/cinemas/12.jpg",
                    "type": "VIP",
                    "status": "OPEN",
                    "is_active": True,
                    "screens": 8,
                    "last_renovation": "2024-08-15",
                    "region": "CDMX_CENTER",
                    "amenities": {
                        "parking": True,
                        "food_court": True,
                        "coffee_station": False,
                        "disabled_access": True,
                    },
                }
            ]
        },
    )


class CinemaDetailResponse(BaseModel):
    """
    Detailed cinema response for get-by-id endpoints.

    Contains most fields required by clients, while omitting a small number of
    fields that are usually internal (e.g. soft-delete timestamps).
    """

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_encoders={date: lambda v: v.isoformat()},
        extra="forbid",
        json_schema_extra={
            "examples": [
                {
                    "id": 12,
                    "image": "https://cdn.example.com/cinemas/12.jpg",
                    "name": "Cinepolis Centro",
                    "tax_number": "TEC-123456",
                    "is_active": True,
                    "description": "Five-screen multiplex with IMAX and VIP seating.",
                    "screens": 5,
                    "last_renovation": "2024-08-15",
                    "type": "VIP",
                    "status": "OPEN",
                    "amenities": {
                        "parking": True,
                        "food_court": True,
                        "coffee_station": False,
                        "disabled_access": True,
                    },
                    "region": "CDMX_CENTER",
                    "location": {"lat": 19.4326, "lng": -99.1332},
                    "contact_info": {
                        "address": "Av. Ejemplo 123, Centro",
                        "phone": "+52-55-1234-5678",
                        "email_contact": "info@cinema.com",
                        "location": {"lat": 19.4326, "lng": -99.1332},
                    },
                    "social_media": {
                        "facebook": "https://facebook.com/cinepolis",
                        "instagram": "https://instagram.com/cinepolis",
                        "x": "https://x.com/cinepolis",
                        "tik_tok": "https://tiktok.com/@cinepolis",
                    },
                    "features": ["IMAX", "VIP_SEATING", "2D"],
                    "created_at": "2025-01-01T10:00:00Z",
                    "updated_at": "2026-01-01T12:00:00Z",
                }
            ]
        },
    )

    id: int = Field(..., description="Unique identifier of the cinema.", examples=[12])
    image: str = Field(
        "",
        description="URL or path to the cinema's main image.",
        examples=["https://cdn.example.com/cinemas/12.jpg"],
    )
    name: str = Field(
        ...,
        max_length=255,
        min_length=3,
        description="Cinema name.",
        examples=["Cinepolis Centro"],
    )
    tax_number: str = Field(
        ...,
        max_length=255,
        min_length=5,
        description="Unique tax identification number.",
        examples=["TEC-123456"],
    )
    is_active: bool = Field(
        False,
        description="Whether the cinema is operational/active.",
        examples=[True],
    )
    description: str = Field(
        "",
        description="Brief description about the cinema.",
        examples=["Five-screen multiplex with IMAX and VIP seating."],
    )
    screens: int = Field(
        ...,
        ge=0,
        description="Number of screens in the cinema.",
        examples=[5],
    )
    last_renovation: Optional[date] = Field(
        None,
        description="Date of the last major renovation (if available).",
        examples=["2024-08-15"],
    )

    type: CinemaType = Field(
        ...,
        description="Cinema type (e.g., VIP, Traditional).",
        examples=[CinemaType.VIP],
    )
    status: CinemaStatus = Field(
        ...,
        description="Current operational status.",
        examples=[CinemaStatus.OPEN],
    )
    amenities: CinemaAmenities = Field(
        ...,
        description="Amenities available at the cinema (e.g., parking, food court).",
    )
    region: LocationRegion = Field(
        ...,
        description="Geographical region where the cinema is located.",
        examples=[LocationRegion.CDMX_CENTER],
    )
    location: Location = Field(
        ...,
        description="Geographical coordinates of the cinema.",
    )
    contact_info: ContactInfo = Field(
        ...,
        description="Contact information for the cinema.",
    )
    social_media: SocialMedia = Field(
        ...,
        description="Social media links.",
    )
    features: List[CinemaFeatures] = Field(
        ...,
        description="Special features offered by the cinema.",
    )
    created_at: datetime = Field(
        ...,
        description="Date/time when the cinema was created.",
    )
    updated_at: datetime = Field(
        ...,
        description="Date/time when the cinema was last updated.",
    )


class CinemaResponse(CinemaDetailResponse):
    """
    Backwards-compatible alias.

    Prefer `CinemaDetailResponse` for new code.
    """


class PaginatedCinemaSummaryResponse(PaginationMetadata):
    """
    Paginated response for cinema list/search endpoints.

    `data` contains `CinemaSummaryResponse` objects for the current page.
    """

    data: List[CinemaSummaryResponse]

    @classmethod
    def from_page(cls, page: "Page[Cinema]") -> "PaginatedCinemaSummaryResponse":
        """
        Convert a Page[Cinema] domain object to PaginatedCinemaSummaryResponse DTO.

        Args:
            page: Page object containing Cinema entities and pagination metadata

        Returns:
            PaginatedCinemaSummaryResponse with converted data
        """
        cinema_summaries = [
            CinemaSummaryResponse.model_validate(cinema) for cinema in page.items
        ]

        return cls(
            data=cinema_summaries,
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
