import logging

from app.shared.notification.domain.entities import Notification
from app.shared.notification.domain.services import NotificationService

logger = logging.getLogger(__name__)


class NotificationServiceImpl(NotificationService):
    async def send_notification(self, notification: Notification) -> None:
        logger.info(
            "notification queued type=%s user_id=%s",
            notification.notification_type.value,
            notification.user.id,
        )
