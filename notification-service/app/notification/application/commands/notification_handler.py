from typing import Dict, Any
from ..usecases.notification_usecases import CreateNotificationUseCase
from .notification_command import CreateNotificationCommand as NotificationCommand


class NotificationHandler:
    def __init__(self, usecase: CreateNotificationUseCase) -> None:
        self.usecase = usecase

    async def handle(self, notification_json: Dict[str, Any]):
        command = NotificationCommand(**notification_json)
        await self.usecase.execute(command)
