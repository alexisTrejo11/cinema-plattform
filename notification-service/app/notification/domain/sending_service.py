from abc import ABC, abstractmethod
from app.notification.domain.entities.models import Notification


class SendingService(ABC):
    """Port for delivering notification payloads through external providers."""

    @abstractmethod
    async def send_notification(self, notification: Notification) -> None:
        raise NotImplementedError
