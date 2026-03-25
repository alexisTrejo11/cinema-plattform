import logging

from app.shared.events.builders import notification_requested
from app.shared.events.protocols import EventPublisher
from app.shared.notification.domain.entities import Notification
from app.shared.notification.domain.services import NotificationService

logger = logging.getLogger(__name__)


class NotificationServiceImpl(NotificationService):
    """
    Publishes ``notification.requested`` events to Kafka for the notification microservice.
    Falls back to structured logging when the publisher is a no-op.
    """

    def __init__(self, event_publisher: EventPublisher) -> None:
        self._event_publisher = event_publisher

    async def send_notification(self, notification: Notification) -> None:
        envelope = notification_requested(notification)
        await self._event_publisher.publish(envelope)
        logger.info(
            "notification event emitted type=%s user_id=%s event_id=%s",
            notification.notification_type.value,
            notification.user.id,
            envelope.event_id,
        )
