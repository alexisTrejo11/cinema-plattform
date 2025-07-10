from asyncio import gather
import logging
from app.notification.domain.entities.models import Notification
from app.notification.domain.repository import NotificationRepository
from app.notification.domain.sending_service import SendingService
from ..commands.notification_command import (
    CreateNotificationCommand as NotificationCommand,
)

logger = logging.getLogger("app")


class CreateNotificationUseCase:
    def __init__(
        self, repository: NotificationRepository, sending_service: SendingService
    ) -> None:
        self.repository = repository
        self.sending_service = sending_service

    async def execute(self, command: NotificationCommand):
        new_notification = Notification.from_dict(**command.model_dump())

        save_coroutine = self.repository.save(new_notification)
        send_couroutine = self.sending_service.send(new_notification)

        _, _ = gather(save_coroutine, send_couroutine)
        logger.info(
            f"Notification:{new_notification.notification_id} for user {new_notification.recipient.user_id}"
        )
