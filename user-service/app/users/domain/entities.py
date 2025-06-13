from .enums import UserRole
from typing import Optional
from datetime import datetime, timezone

class User:
    def __init__(
        self,
        user_id: str,
        email: str,
        username: str,
        hashed_password: str,
        role: UserRole = UserRole.USER,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.user_id = user_id
        self.email = email
        self.username = username
        self.hashed_password = hashed_password
        self.role = role
        self.is_active = is_active
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)
        
    def update_password(self, new_hashed_password: str):
        self.hashed_password = new_hashed_password
        self.updated_at = datetime.now(timezone.utc)
    
    def deactivate(self):
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)
    
    def activate(self):
        self.is_active = True
        self.updated_at = datetime.now(timezone.utc)