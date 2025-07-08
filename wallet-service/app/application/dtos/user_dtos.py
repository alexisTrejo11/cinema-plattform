from pydantic import BaseModel, Field
from uuid import UUID


class UserResponse(BaseModel):
    """Data Transfer Object for user information."""

    id: UUID
    username: str
    email: str
    role: str

    class Config:
        orm_mode = True


class CreateUserResponse(BaseModel):
    """Data Transfer Object for creating a new user."""

    username: str = Field(..., description="The username for the new user.")
    email: str = Field(..., description="The email address for the new user.")
    role: str
