from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from app.domain.models import User


class UserRepository(ABC):
    """Abstract repository for user data access."""

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        """Retrieves a user by their ID."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """Retrieves a user by their email address."""
        raise NotImplementedError

    @abstractmethod
    async def create(self, user: User) -> User:
        """Creates a new user."""
        raise NotImplementedError
