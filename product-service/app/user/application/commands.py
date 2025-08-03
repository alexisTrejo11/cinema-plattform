from pydantic import BaseModel, ConfigDict, Field
from pydantic.networks import EmailStr
from typing import List, Optional
from app.user.domain.value_objects import UserRole, UserId


class UserCreateCommand(BaseModel):
    user_id: UserId
    email: EmailStr
    roles: List[UserRole] = Field(default_factory=list)
    is_active: bool = True

    model_config = ConfigDict(arbitrary_types_allowed=True)


class UserUpdateCommand(BaseModel):
    email: Optional[EmailStr]
    roles: Optional[List[UserRole]] = Field(default_factory=list)
    is_active: Optional[bool] = True

    model_config = ConfigDict(arbitrary_types_allowed=True)
