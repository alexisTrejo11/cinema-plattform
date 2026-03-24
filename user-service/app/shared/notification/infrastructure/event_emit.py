from app.notification.application.services import NotificationService
from app.notification.domain.entitites import Notification
from app.config.queue.rabbitmq import rabbitmq_publisher
import logging

logger = logging.getLogger("app")


class NotificationServiceImpl(NotificationService):
    async def send_notification(self, notification: Notification):
        await rabbitmq_publisher.connect()

        user = notification.user
        logger.info(
            f"Attempting to send {notification.notification_type.value} notification to {user.email} with token: {notification.token[:2]}"
        )

        await rabbitmq_publisher.publish_token_request(
            user_email=user.email,
            token=notification.token,
            notification_type=notification.notification_type.value,
        )

        await rabbitmq_publisher.close()
