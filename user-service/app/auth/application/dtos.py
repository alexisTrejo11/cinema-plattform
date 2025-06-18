from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.users.domain.entities import Profile

class SignUpRequest(Profile):
    email: EmailStr
    phone_number: Optional[str] = Field(None, min_length=6)
    password: str

class LoginRequest(BaseModel):
    identifier_field: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in_minutes: int


class RefreshTokenRequest(BaseModel):
    refresh_token: str
