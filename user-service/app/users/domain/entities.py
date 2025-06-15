from .enums import UserRole, Gender
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, PastDate

class UserBase(BaseModel):
    email: EmailStr
    gender: Gender
    phone_number: str = Field(..., min_length=6)
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    date_of_birth: PastDate


class User(UserBase):
    id: int = 0
    hashed_password: str = Field(..., min_length=8)
    role: UserRole = UserRole.CUSTOMER
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    is_active: bool = True
        
    def update_password(self, new_hashed_password: str):
        self.hashed_password = new_hashed_password
        self.updated_at = datetime.now()
    
    def deactivate(self):
        self.is_active = False
        self.updated_at = datetime.now()
    
    def activate(self):
        self.is_active = True
        self.updated_at = datetime.now()