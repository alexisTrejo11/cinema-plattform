from typing import Optional, Dict, Any, List
from app.notification.domain.entities.models import Notification
from abc import ABC, abstractmethod
from uuid import UUID


class NotificationRepository(ABC):
    """
    Abstract Base Class for notification repository operations.
    Defines the contract for data access specific to notifications.
    """

    @abstractmethod
    async def get_by_id(self, notification_id: UUID) -> Optional[Notification]:
        """Retrieves a single notification by its unique ID."""
        pass

    @abstractmethod
    async def list_by_type(
        self, notification_type: str, limit: int, offset: int
    ) -> List[Notification]:
        """Lists notifications by their type, with pagination."""
        pass

    @abstractmethod
    async def list_by_channel(
        self, channel: str, limit: int, offset: int
    ) -> List[Notification]:
        """Lists notifications by their channel, with pagination."""
        pass

    @abstractmethod
    async def list_by_user_id(
        self, user_id: UUID, limit: int, offset: int
    ) -> List[Notification]:
        """Lists notifications for a specific user ID, with pagination."""
        pass

    @abstractmethod
    async def list_by_status(
        self, status: str, limit: int, offset: int
    ) -> List[Notification]:
        """Lists notifications by their status, with pagination."""
        pass

    @abstractmethod
    async def count_by_type(self, notification_type: str) -> int:
        """Counts notifications by their type."""
        pass

    @abstractmethod
    async def count_by_channel(self, channel: str) -> int:
        """Counts notifications by their channel."""
        pass

    @abstractmethod
    async def count_by_user_id(self, user_id: UUID) -> int:
        """Counts notifications by their user ID."""
        pass

    @abstractmethod
    async def count_by_status(self, status: str) -> int:
        """Counts notifications by their status."""
        pass

    @abstractmethod
    async def save(self, notification: Notification) -> Notification:
        pass
