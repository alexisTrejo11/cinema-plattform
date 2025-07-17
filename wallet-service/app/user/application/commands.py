from pydantic import BaseModel, Field
from pydantic.networks import EmailStr
from typing import List, Optional
from app.user.domain.value_objects import UserRole, UserId


class UserCreateCommand(BaseModel):
    user_id: UserId
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
