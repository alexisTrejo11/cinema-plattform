from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.application.repositories import UserRepository
from app.users.domain.entities import User
from app.users.domain.exceptions import *
from app.users.domain.entities import User
from .models import UserModel

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, user: User) -> User:
        user_model = UserModel.from_domain(user)

        self.session.add(user_model)
        await self.session.commit()
               
        return user_model.to_domain()
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        return user_model.to_domain() if user_model else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user_model = result.scalar_one_or_none()
        return user_model.to_domain() if user_model else None
    
    async def get_by_phone(self, phone: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.phone_number == phone)
        )
        user_model = result.scalar_one_or_none()
        return user_model.to_domain() if user_model else None
    
    async def update(self, user: User) -> User:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user.id))
        
        user_model = result.scalar_one_or_none()
        if not user_model:
            raise UserNotFoundException("User not found")
        
        user_model.update_from_domain(user)
        await self.session.commit()
        await self.session.refresh(user_model)
        return user_model.to_domain()
    
    async def delete(self, user_id: int) -> bool:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        
        user_model = result.scalar_one_or_none()
        if not user_model:
            return False
        
        await self.session.delete(user_model)
        await self.session.commit()
        
        return True
    
    async def list_users(self, size: int = 0, number: int = 100) -> List[User]:
        result = await self.session.execute(select(UserModel).offset(size).limit(number))
        user_models = result.scalars().all()
        
        return [user_model.to_domain() for user_model in user_models]