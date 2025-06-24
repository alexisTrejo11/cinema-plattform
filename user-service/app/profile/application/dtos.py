from pydantic import BaseModel, Field, PastDate
from app.users.domain.enums import Gender
from typing import Optional
from datetime import date, datetime

class BaseProfile(BaseModel):
    """
    Represents a user's detailed  base profile information.
    """
    gender: Gender = Field(
        ...,
        description="The gender of the user.",
        examples=[Gender.MALE]
    )
    first_name: str = Field(
        ...,
        min_length=3,
        description="The first name of the user.",
        examples=["John", "Jane"]
    )
    last_name: Optional[str] = Field(
        None,
        min_length=3,
        description="The last name of the user. Optional.",
        examples=["Doe", "Smith"]
    )
    date_of_birth: PastDate = Field(
        ...,
        description="The user's date of birth. Must be a past date.",
        examples=["1990-01-15", "1985-07-22"]
    )

class Profile(BaseProfile):
    """
    Represents a user's detailed profile information.
    """
    

class ProfileResponse(Profile):
    """
    Represents the full profile data returned in API responses.
    Inherits all fields and documentation from the Profile base model.
    """
    pass
    
    class Config:
        """
        Pydantic configuration for the Profile model.
        """
        json_schema_extra = {
            "example": {
                "gender": "MALE",
                "first_name": "Alice",
                "last_name": "Johnson",
                "date_of_birth": "1992-05-20",
            }
        }


class ProfileUpdate(BaseModel):
    """
    Represents the data for updating a user's profile.
    All fields are optional, allowing for partial updates.
    """
    gender: Optional[Gender] = Field(
        None,
        description="Optional: The updated gender of the user.",
        examples=[Gender.FEMALE]
    )
    first_name: Optional[str] = Field(
        None,
        min_length=3,
        description="Optional: The updated first name of the user.",
        examples=["Robert"]
    )
    last_name: Optional[str] = Field(
        None,
        min_length=3,
        description="Optional: The updated last name of the user.",
        examples=["Brown"]
    )
    date_of_birth: Optional[date] = Field(
        None,
        description="Optional: The updated date of birth for the user.",
        examples=["1988-11-01"]
    )

    class Config:
        """
        Pydantic configuration for the ProfileUpdate model.
        """
        json_schema_extra = {
            "example": {
                "first_name": "Bob",
                "date_of_birth": "1995-03-25"
            }
        }