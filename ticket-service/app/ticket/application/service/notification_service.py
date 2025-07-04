from abc import ABC, abstractmethod
from app.notification.notification import Notification

class NotificationService(ABC):
    @abstractmethod
    async def send_notification(self, notification: Notification):
        pass