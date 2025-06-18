from pydantic import BaseModel, Field, PastDate
from app.users.domain.enums import Gender
from typing import Optional
from datetime import date

class Profile(BaseModel):
    gender: Gender
    first_name: str = Field(..., min_length=3)
    last_name:  Optional[str] = Field(None, min_length=3)
    date_of_birth: PastDate
    #joined_date: datetime = Field(default=datetime.now())


class ProfileResponse(Profile):
    pass


class ProfileUpdate(BaseModel):
    gender: Optional[Gender] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
