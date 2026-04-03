import logging

from app.notification.application.commands.notification_command import (
    CreateNotificationCommand,
)
from app.notification.application.dtos import NotificationListResponse, NotificationResponse
from app.notification.application.queries.notification_queries import (
    GetNotificationByIdQuery,
    ListNotificationsQuery,
)
from app.notification.domain.entities.models import Notification
from app.notification.domain.repository import NotificationRepository
from app.notification.domain.sending_service import SendingService

logger = logging.getLogger("app")


class CreateNotificationUseCase:
    def __init__(
        self, repository: NotificationRepository, sending_service: SendingService
    ) -> None:
        self.repository = repository
        self.sending_service = sending_service

    async def execute(self, command: CreateNotificationCommand) -> NotificationResponse:
        notification = Notification(
            notification_type=command.notification_type,
            recipient=command.recipient,
            content=command.content,
            channel=command.channel,
            event_id=command.event_id,
        )
        saved = await self.repository.save(notification)
        await self.sending_service.send_notification(saved)
        logger.info(
            "notification.created id=%s user_id=%s channel=%s type=%s",
            saved.notification_id,
            saved.recipient.user_id,
            saved.channel.value,
            saved.notification_type.value,
        )
        return NotificationResponse.model_validate(saved.model_dump())


class GetNotificationByIdUseCase:
    def __init__(self, repository: NotificationRepository) -> None:
        self.repository = repository

    async def execute(self, query: GetNotificationByIdQuery) -> NotificationResponse | None:
        notification = await self.repository.get_by_id(query.notification_id)
        if notification is None:
            return None
        return NotificationResponse.model_validate(notification.model_dump())


class ListNotificationsUseCase:
    def __init__(self, repository: NotificationRepository) -> None:
        self.repository = repository

    async def execute(self, query: ListNotificationsQuery) -> NotificationListResponse:
        notifications = await self.repository.list_notifications(
            notification_type=query.notification_type,
            channel=query.channel,
            user_id=query.user_id,
            status=query.status,
            limit=query.limit,
            offset=query.offset,
        )
        total_count = await self.repository.count_notifications(
            notification_type=query.notification_type,
            channel=query.channel,
            user_id=query.user_id,
            status=query.status,
        )
        return NotificationListResponse(
            notifications=[
                NotificationResponse.model_validate(item.model_dump())
                for item in notifications
            ],
            total_count=total_count,
        )
