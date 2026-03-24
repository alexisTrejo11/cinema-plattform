from app.notification.application.services import NotificationService
from app.notification.domain.entitites import Notification
import logging

logger = logging.getLogger("app")


class NotificationServiceImpl(NotificationService):
    async def send_notification(self, notification: Notification):
        logger.info(f"Sending notification to {notification.user.email}")
        # TODO: Implement notification sending
        pass
