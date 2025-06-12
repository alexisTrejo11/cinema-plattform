from pydantic import BaseModel, EmailStr
from typing import Optional

class Location(BaseModel):
    lat: float
    lng: float


class ContactInfo(BaseModel):
    address: str
    phone: str
    email_contact: EmailStr
    location: Location 


class SocialMedia(BaseModel):
    facebook: Optional[str]
    instagram: Optional[str]
    x: Optional[str]
    tik_tok: Optional[str]


class CinemaAmenities(BaseModel):
    parking: bool = False
    food_court: bool = False
    coffee_station: bool = False
    disabled_access: bool = False


