from abc import ABC, abstractmethod
from typing import List, Optional
from typing import Dict, Any
from app.user.domain.user import User


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Retrieve a user by their ID."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email."""
        pass

    @abstractmethod
    async def list(self, params: Dict[str, Any]) -> List[User]:
        """Retrieve all users."""
        pass

    @abstractmethod
    async def save(self, user_data: dict) -> User:
        """Create a new user."""
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """Delete a user by their ID."""
        pass
