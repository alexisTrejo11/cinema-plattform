from abc import ABC, abstractmethod
from app.notification.domain.entities.models import Notification


class SendingService:
    @abstractmethod
    async def send(self, notification: Notification) -> None:
        pass
