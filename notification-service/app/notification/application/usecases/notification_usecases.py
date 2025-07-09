from ..commands.notification_command import (
    CreateNotificationCommand as NotificationCommand,
)
from app.domain.entities.models import Notification
from app.domain.repository import NotificationRepository
from asyncio import gather


class CreateNotificationUseCase:
    def __init__(self, repository: NotificationRepository) -> None:
        self.repository = repository

    async def execute(self, command: NotificationCommand):
        new_notification = Notification.from_dict(**command.model_dump())

        save_coroutine = self.repository.save(new_notification)
        send_couroutine = self._send(new_notification)
        _, _ = gather(save_coroutine, send_couroutine)

        print("Success")

    async def _send(self, notification: Notification):
        pass
