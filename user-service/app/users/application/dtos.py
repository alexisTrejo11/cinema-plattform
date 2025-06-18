from pydantic import Field, BaseModel, EmailStr
from app.users.domain.entities import User
from app.users.domain.enums import Gender
from app.profile.application.dtos import Profile 
from typing import Optional
from datetime import date

class UserCreate(Profile):
    password: str = Field(..., min_length=8)
    email: EmailStr
    phone_number: str = Field(..., min_length=6)
    
    def to_domain(self) -> 'User':
        return User(**self.model_dump())
    
    
class UserResponse(Profile):
    id: int
    
    @staticmethod
    def from_domain(entity: User) -> 'UserResponse':
        return UserResponse(**entity.model_dump())
    

class UserUpdate(BaseModel):
    password: str
    email: EmailStr
    gender: Gender
    phone_number: str
    first_name: str 
    last_name: str
    date_of_birth: date
    
    def update_user_fields(self, entity: User, hashed_password: Optional[str] = None) -> User:
        update_data = self.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            if key != 'password':
                setattr(entity, key, value)
            
        if hashed_password:
            entity.password = hashed_password
        
        return entity
    