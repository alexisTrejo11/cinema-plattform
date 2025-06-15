from pydantic import Field, BaseModel, EmailStr
from app.users.domain.entities import User, UserBase, Gender
from typing import Optional
from datetime import date

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    def to_domain(self, hashed_password: str) -> 'User':
        return User(hashed_password=hashed_password, **self.model_dump())
    
class UserResponse(UserBase):
    id: int
    
    @staticmethod
    def from_domain(entity: User) -> 'UserResponse':
        return UserResponse(**entity.model_dump())
    

class Profile(UserBase):
    pass

class UserUpdate(BaseModel):
    password: str
    email: EmailStr
    gender: Gender
    phone_number: str
    first_name: str 
    last_name: str
    date_of_birth: date
    
    
    def update_user_fields(self, entity: User, hashed_password: Optional[str]) -> User:
        update_data = self.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            if key != 'password':
                setattr(entity, key, value)
            
        if hashed_password:
            entity.hashed_password = hashed_password
        
        return entity