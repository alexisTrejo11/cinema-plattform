from typing import Any, Optional
from .enums import UserRole, Gender
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, PastDate

class Profile(BaseModel):
    gender: Gender
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    date_of_birth: PastDate
    joined_date: datetime = Field(default=datetime.now())


class Account(Profile):
    id: Optional[int] = None
    email: EmailStr
    phone_number: str = Field(..., min_length=6)
    hashed_password: str = Field(..., min_length=8)
    role: UserRole = UserRole.CUSTOMER
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    is_active: bool = True
    
    
class User(Account):
    
    def update_profile(self, **kwargs: Any) -> None:
        """
        Updates the user's profile information based on provided keyword arguments.
        Only updates fields that are explicitly present in kwargs.
        """
        updatable_fields = ["email", "gender", "phone_number", "first_name", "last_name", "date_of_birth"]


        for field_name in updatable_fields:
            if field_name in kwargs:
                new_value = kwargs[field_name]

                setattr(self, field_name, new_value)

        self.updated_at = datetime.now()
    
    def update_password(self, new_hashed_password: str):
        self.hashed_password = new_hashed_password
        self.updated_at = datetime.now()
    
    def deactivate(self):
        self.is_active = False
        self.updated_at = datetime.now()
    
    def activate(self):
        self.is_active = True
        self.updated_at = datetime.now()