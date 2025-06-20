from ..domain.entitites import Notification
from abc import ABC, abstractmethod

class NotificationService(ABC):
    @abstractmethod
    async def send_notification(self, notification: Notification) -> None:
        pass
    