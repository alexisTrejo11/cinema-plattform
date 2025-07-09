from abc import ABC, abstractmethod
from typing import Optional, List
from .entities.user import User, UserRole


class UserRepository(ABC):
    """Abstract repository for User entity"""
    
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass
    
    @abstractmethod
    async def get_by_phone(self, phone: str) -> Optional[User]:
        """Get user by phone"""
        pass
    
    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user"""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """Update an existing user"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """Hard delete a user"""
        pass
    
    @abstractmethod
    async def soft_delete(self, user_id: str) -> bool:
        """Soft delete a user"""
        pass
    
    @abstractmethod
    async def restore(self, user_id: str) -> bool:
        """Restore a soft deleted user"""
        pass
    
    @abstractmethod
    async def get_active_users(self) -> List[User]:
        """Get all active users (not deleted)"""
        pass
    
    @abstractmethod
    async def get_users_by_role(self, role: UserRole) -> List[User]:
        """Get users by role"""
        pass
    
    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email"""
        pass
    
    @abstractmethod
    async def exists_by_phone(self, phone: str) -> bool:
        """Check if user exists by phone"""
        pass
