from pydantic import BaseModel, EmailStr
from app.users.domain.entities import UserBase


class SignUpRequest(UserBase):
    password: str    

class LoginRequest(BaseModel):
    identifier_field: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

 
class RefreshTokenRequest(BaseModel):
    refresh_token: str
