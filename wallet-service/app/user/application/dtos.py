from pydantic import BaseModel, Field
from uuid import UUID
from pydantic.networks import EmailStr
from datetime import datetime
from typing import List, Optional
from app.user.domain.value_objects import UserRole


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    roles: List[UserRole]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        use_enum_values = True


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
