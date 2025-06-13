from datetime import datetime
from pydantic import BaseModel
from app.users.domain.enums import UserRole

class UserResponse(BaseModel):
    user_id: str
    email: str
    username: str
    role: UserRole
    is_active: bool
    created_at: datetime