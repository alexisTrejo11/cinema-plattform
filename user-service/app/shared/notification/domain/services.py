from abc import ABC, abstractmethod

from .entities import Notification


class NotificationService(ABC):
    @abstractmethod
    async def send_notification(self, notification: Notification) -> None:
        pass
