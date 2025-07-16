from pydantic import BaseModel, Field
from uuid import UUID
from pydantic.networks import EmailStr
from datetime import datetime
from typing import List, Optional
from app.user.domain.value_objects import UserRole


class UserResponse(BaseModel):
    id: UUID = Field(
        ...,
        description="The unique identifier for the user.",
        json_schema_extra={"example": "a1b2c3d4-e5f6-7890-1234-567890abcdef"}
    )
    email: EmailStr = Field(
        ...,
        description="The user's email address, used for login.",
        json_schema_extra={"example": "user@example.com"}
    )
    roles: List[UserRole] = Field(
        ...,
        description="A list of roles assigned to the user, defining their permissions within the system.",
        json_schema_extra={"example": ["user", "admin"]}
    )
    is_active: bool = Field(
        ...,
        description="Indicates whether the user's account is active and can log in.",
        json_schema_extra={"example": True}
    )
    created_at: datetime = Field(
        ...,
        description="The date and time when the user's account was created (ISO 8601 format).",
        json_schema_extra={"example": "2024-07-15T10:30:00.123456Z"}
    )

    model_config = {
        "from_attributes": True,
        "use_enum_values": True,
        "json_schema_extra": {
            "example": {
                "id": "f5e4d3c2-b1a0-9876-5432-10fedcba9876",
                "email": "example@domain.com",
                "roles": ["user"],
                "is_active": True,
                "created_at": "2024-07-15T10:30:00.123456Z"
            }
        }
    }

class PydanticUserId(BaseModel):
    value: UUID

    class Config:
        arbitrary_types_allowed = True


class UserCreateCommand(BaseModel):
    email: EmailStr
    roles: List[UserRole] = Field(default_factory=list)
    is_active: bool = True

    class Config:
        use_enum_values = True


class UserUpdateCommand(BaseModel):
    email: Optional[EmailStr]
    roles: Optional[List[UserRole]] = Field(default_factory=list)
    is_active: Optional[bool] = True

    class Config:
        use_enum_values = True
