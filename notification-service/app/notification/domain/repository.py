from abc import ABC, abstractmethod
from typing import List, Optional

from app.notification.domain.entities.models import Notification
from app.notification.domain.enums import (
    NotificationChannel,
    NotificationStatus,
    NotificationType,
)


class NotificationRepository(ABC):
    """
    Abstract Base Class for notification repository operations.
    Defines the contract for data access specific to notifications.
    """

    @abstractmethod
    async def get_by_id(self, notification_id: str) -> Optional[Notification]:
        """Retrieves a single notification by its unique ID."""
        raise NotImplementedError

    @abstractmethod
    async def list_notifications(
        self,
        *,
        notification_type: Optional[NotificationType] = None,
        channel: Optional[NotificationChannel] = None,
        user_id: Optional[str] = None,
        status: Optional[NotificationStatus] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> List[Notification]:
        """Lists notifications by optional filters with pagination."""
        raise NotImplementedError

    @abstractmethod
    async def count_notifications(
        self,
        *,
        notification_type: Optional[NotificationType] = None,
        channel: Optional[NotificationChannel] = None,
        user_id: Optional[str] = None,
        status: Optional[NotificationStatus] = None,
    ) -> int:
        """Counts notifications by optional filters."""
        raise NotImplementedError

    @abstractmethod
    async def save(self, notification: Notification) -> Notification:
        raise NotImplementedError
