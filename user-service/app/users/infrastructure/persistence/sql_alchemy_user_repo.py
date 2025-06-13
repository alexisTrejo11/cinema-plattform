from typing import Optional, List
from app.users.application.repositories import UserRepository
from app.users.domain.entities import User


class SqlAlchemyUserRepo(UserRepository):
    async def create(self, user: User) -> User:
        pass
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        pass
    
    async def get_by_email(self, email: str) -> Optional[User]:
        pass
    
    async def get_by_username(self, username: str) -> Optional[User]:
        pass
    
    async def update(self, user: User) -> User:
        pass
    
    async def delete(self, user_id: str) -> bool:
        pass
    
    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        pass

    