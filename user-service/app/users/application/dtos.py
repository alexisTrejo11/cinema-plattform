from pydantic import Field, BaseModel, EmailStr
from app.users.domain import User, Gender, Status, UserRole
from app.profile.application.dtos import BaseProfile
from typing import Optional
from datetime import date, datetime


class UserCreate(BaseProfile):
    """
    Represents the data required to create a new user.
    It inherits profile-related fields from the `Profile` DTO.
    """

    password: str = Field(
        ...,
        min_length=8,
        description="The user's password. Must be at least 8 characters long.",
        examples=["SecureP@ss123"],
    )
    email: EmailStr = Field(
        ...,
        description="The user's unique email address.",
        examples=["john.doe@example.com"],
    )
    phone_number: str = Field(
        ...,
        min_length=6,
        description="The user's phone number.",
        examples=["+1234567890", "5512345678"],
    )

    class Config:
        """
        Pydantic configuration for the UserCreate model.
        """

        json_schema_extra = {
            "example": {
                "gender": "MALE",
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1990-01-15",
                "password": "MySuperSecretPassword1!",
                "email": "john.doe@example.com",
                "phone_number": "+1234567890",
            }
        }

    def to_domain(self) -> "User":
        """
        Converts the UserCreate DTO to a User domain entity.
        """
        return User.model_validate(self.model_dump())


class UserResponse(BaseProfile):
    """
    Represents a sanitized user payload returned by user API endpoints.
    This model intentionally excludes sensitive fields such as `password`.
    """

    id: int = Field(
        ..., description="The unique identifier of the user.", examples=[1, 101]
    )
    email: EmailStr = Field(
        ...,
        description="The user's unique email address.",
        examples=["jane.smith@example.com"],
    )
    phone_number: Optional[str] = Field(
        None,
        description="Phone number associated with the user account.",
        examples=["+1234567890"],
    )
    role: UserRole = Field(
        ...,
        description="Role assigned to the user in the platform.",
        examples=[UserRole.CUSTOMER],
    )
    status: Status = Field(
        ...,
        description="Current account state used to allow or restrict access.",
        examples=[Status.ACTIVE],
    )
    is_2fa_enabled: bool = Field(
        ...,
        description="Whether two-factor authentication is enabled for the account.",
        examples=[True, False],
    )
    created_at: datetime = Field(
        ...,
        description="UTC timestamp when the account was created.",
        examples=["2026-03-22T14:55:03.421000"],
    )
    updated_at: datetime = Field(
        ...,
        description="UTC timestamp of the most recent account update.",
        examples=["2026-03-23T10:12:45.112000"],
    )

    class Config:
        """
        Pydantic configuration for the UserResponse model.
        """

        json_schema_extra = {
            "example": {
                "id": 123,
                "gender": "FEMALE",
                "first_name": "Jane",
                "last_name": "Smith",
                "date_of_birth": "1992-03-20",
                "email": "jane.smith@example.com",
                "phone_number": "+1234567890",
                "role": "CUSTOMER",
                "status": "ACTIVE",
                "is_2fa_enabled": True,
                "created_at": "2026-03-22T14:55:03.421000",
                "updated_at": "2026-03-23T10:12:45.112000",
            }
        }

    @staticmethod
    def from_domain(entity: User) -> "UserResponse":
        """
        Maps a User domain model into a safe API response model.
        """
        return UserResponse.model_validate(entity.model_dump())


class UserUpdate(BaseModel):
    """
    Represents the data available for updating an existing user's details.
    All fields are optional, allowing for partial updates.
    """

    password: Optional[str] = Field(
        None,
        min_length=8,
        description="Optional: The new password for the user. Must be at least 8 characters long if provided.",
        examples=["NewP@ssword!"],
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Optional: The new email address for the user.",
        examples=["new.email@example.com"],
    )
    gender: Optional[Gender] = Field(
        None,
        description="Optional: The new gender for the user.",
        examples=[Gender.FEMALE],
    )
    phone_number: Optional[str] = Field(
        None,
        min_length=6,
        description="Optional: The new phone number for the user.",
        examples=["+1987654321"],
    )
    first_name: Optional[str] = Field(
        None,
        min_length=3,
        description="Optional: The new first name for the user.",
        examples=["Robert"],
    )
    last_name: Optional[str] = Field(
        None,
        min_length=3,
        description="Optional: The new last name for the user.",
        examples=["Johnson"],
    )
    date_of_birth: Optional[date] = Field(
        None,
        description="Optional: The new date of birth for the user.",
        examples=["1985-11-20"],
    )

    class Config:
        """
        Pydantic configuration for the UserUpdate model.
        """

        json_schema_extra = {
            "example": {
                "email": "updated.email@example.com",
                "first_name": "Roberto",
                "phone_number": "9987654321",
            }
        }

    def update_user_fields(
        self, entity: User, hashed_password: Optional[str] = None
    ) -> User:
        """
        Updates the fields of a User domain entity with the provided data.
        Only fields that are set in the UserUpdate DTO will be updated.
        """
        update_data = self.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if key != "password":
                setattr(entity, key, value)

        if hashed_password:
            entity.password = hashed_password

        return entity
