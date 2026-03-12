from datetime import date
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from .enums import CinemaType, CinemaStatus, CinemaFeatures, LocationRegion
from .value_objects import ContactInfo, Location, SocialMedia, CinemaAmenities

class CinemaBase(BaseModel):
    """Base model containing all cinema fields with common configurations"""
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_encoders={date: lambda v: v.isoformat()},
        extra='forbid'
    )

    image: str = Field('', description="URL or path to the cinema's main image.")
    name: str = Field(..., max_length=255, min_length=3, description="Name of the cinema.")
    tax_number: str = Field(..., max_length=255, min_length=5, description="Unique tax identification number.")
    is_active: bool = Field(False, description="True if the cinema is currently operational.")
    description: str = Field('', description="A brief description of the cinema.")
    screens: int = Field(..., ge=0, description="Number of screens/theaters in the cinema.")
    last_renovation: Optional[date] = Field(None, description="Date of the last major renovation.")

    type: CinemaType = Field(..., description="Type of cinema (e.g., VIP, Traditional).")
    status: CinemaStatus = Field(..., description="Current operational status.")
    amenities: CinemaAmenities = Field(..., description="Details about amenities available.")
    region: LocationRegion = Field(..., description="Region location of the cinema")

    contact_info: ContactInfo = Field(..., description="Contact information.")
    social_media: SocialMedia = Field(..., description="Social media links.")
    features: List[CinemaFeatures] = Field(..., description="Special features offered.")

    @field_validator('last_renovation')
    @classmethod
    def validate_last_renovation_not_future(cls, v: Optional[date]) -> Optional[date]:
        """Ensures the last renovation date is not in the future."""
        if v is not None and v > date.today():
            raise ValueError('Last renovation date cannot be in the future.')
        return v