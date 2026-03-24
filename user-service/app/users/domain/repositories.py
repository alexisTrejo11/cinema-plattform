from typing import Optional, List
from app.users.domain.entities import User
from abc import abstractmethod, ABC


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def get_by_phone(self, phone: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def save(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        pass
    
    @abstractmethod
    async def list_users(self, offset: int = 0, limit: int = 100) -> List[User]:
        pass
