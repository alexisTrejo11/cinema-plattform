from app.notification.domain.sending_service import SendingService
from app.notification.domain.entities.models import Notification
from app.notification.domain.enums import NotificationChannel
from .email.mail_service import EmailService
from .message.sms_message_services import SmsMessageService
import logging

logger = logging.getLogger("app")


class SendingServiceImplementation(SendingService):
    def __init__(
        self, email_service: EmailService, sms_service: SmsMessageService
    ) -> None:
        self.email_service = email_service
        self.sms_service = sms_service

    async def send_notification(self, notification: Notification) -> None:
        match notification.channel:
            case NotificationChannel.EMAIL:
                await self.email_service.send(notification)
            case NotificationChannel.SMS:
                await self.sms_service.send(notification)
            case _:
                logger.info(
                    "channel not yet implemented channel=%s notification_id=%s",
                    notification.channel.value,
                    notification.notification_id,
                )
