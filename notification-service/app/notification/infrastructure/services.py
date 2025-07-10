from app.notification.domain.sending_service import SendingService
from app.notification.domain.entities.models import Notification, NotificationChannel
from .email.mail_service import EmailService
from .message.sms_message_services import SmsMessageService


class SedingServiceImplmentation(SendingService):
    def __init__(
        self, email_service: EmailService, sms_service: SmsMessageService
    ) -> None:
        self.email_service = email_service
        self.sms_service = sms_service

    # TODO: Strategy???
    async def send(self, notification: Notification) -> None:
        match notification.channel:
            case NotificationChannel.EMAIL:
                await self.email_service.send(notification)
            case NotificationChannel.SMS:
                await self.sms_service.send(notification)
            case _:
                raise ValueError(
                    f"notificaition channel {notification.channel} not implemented"
                )
