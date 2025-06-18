import re
from pydantic import EmailStr, Field
from typing import Any, Optional
from datetime import datetime
from .enums import UserRole, Status
from .exceptions import PasswordValidationError
from app.profile.application.dtos import Profile

class Account(Profile):
    email: EmailStr
    phone_number: Optional[str] = Field(None, min_length=6)
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.CUSTOMER
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    status: Status = Field(default=Status.PENDING)
    is_two_fa_auth: bool = False 

    
class User(Account):
    id: int = 0

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
    
    def update_password(self, new_password: str):
        self.password = new_password
        self.updated_at = datetime.now()
    
    def deactivate(self):
        self.status = Status.INACTIVE
        self.updated_at = datetime.now()
    
    def activate(self):
        self.status = Status.ACTIVE
        self.updated_at = datetime.now()
    
    def ban(self):
        self.status = Status.BANNED
        self.updated_at = datetime.now()
        
    @staticmethod
    def validate_password_before_hash(password: str):
        """
        Validates if a given password meets the strong password criteria using regular expressions.

        Criteria:
        - Minimum 8 characters in length.
        - Contains at least one uppercase letter.
        - Contains at least one lowercase letter.
        - Contains at least one digit.
        - Contains at least one special character from the set: !@#$%^&*()_+-=[]{}|;:'",.<>/?~

        Args:
            password (str): The password string to validate.
        
        Raise:
            PasswordValidationError
        
        Returns:
            None
        """        
        password_regex = re.compile(
            r"""
            (?=.*[a-z])
            (?=.*[A-Z])(?=.*\d)
            (?=.*[!@#$%^&*()_+\-=\[\]{}|;:'",.<>/?~])
            .{8,}
            $
            """, re.VERBOSE
        )
        
        if not password_regex.fullmatch(password):
            raise PasswordValidationError("Password", "not strong enough")
    

