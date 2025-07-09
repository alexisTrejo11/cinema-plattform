from typing import Optional, List
from uuid import UUID
from .notification_queries import (
    GetNotificationByIdQuery,
    ListNotificationsByTypeQuery,
    ListNotificationsByChannelQuery,
    ListNotificationsByUserIdQuery,
    ListNotificationsByStatusQuery,
)
from app.application.dtos import NotificationResponse, NotificationListResponse
from app.domain.repository import NotificationRepository


class GetNotificationByIdQueryHandler:
    """
    Handles the GetNotificationByIdQuery to retrieve a single notification.
    """

    def __init__(self, repository: NotificationRepository) -> None:
        self.repository = repository

    async def handle(
        self, query: GetNotificationByIdQuery
    ) -> Optional[NotificationResponse]:
        """
        Processes the GetNotificationByIdQuery.
        """
        notification = await self.repository.get_by_id(query.notification_id)
        if not notification:
            return None

        return NotificationResponse(**notification.to_dict())


class ListNotificationsByTypeQueryHandler:
    """
    Handles the ListNotificationsByTypeQuery to retrieve notifications by type.
    """

    def __init__(self, repository: NotificationRepository):
        self.repository = repository

    async def handle(
        self, query: ListNotificationsByTypeQuery
    ) -> NotificationListResponse:
        """
        Processes the ListNotificationsByTypeQuery.
        """
        notifications = await self.repository.list_by_type(
            query.notification_type, query.limit, query.offset
        )
        total_count = await self.repository.count_by_type(query.notification_type)
        return NotificationListResponse(
            notifications=[NotificationResponse(**n.to_dict()) for n in notifications],
            total_count=total_count,
        )


class ListNotificationsByChannelQueryHandler:
    """
    Handles the ListNotificationsByChannelQuery to retrieve notifications by channel.
    """

    def __init__(self, repository: NotificationRepository):
        self.repository = repository

    async def handle(
        self, query: ListNotificationsByChannelQuery
    ) -> NotificationListResponse:
        """
        Processes the ListNotificationsByChannelQuery.
        """
        notifications = await self.repository.list_by_channel(
            query.channel, query.limit, query.offset
        )
        total_count = await self.repository.count_by_channel(query.channel)
        return NotificationListResponse(
            notifications=[NotificationResponse(**n.to_dict()) for n in notifications],
            total_count=total_count,
        )


class ListNotificationsByUserIdQueryHandler:
    """
    Handles the ListNotificationsByUserIdQuery to retrieve notifications by user ID.
    """

    def __init__(self, repository: NotificationRepository):
        self.repository = repository

    async def handle(
        self, query: ListNotificationsByUserIdQuery
    ) -> NotificationListResponse:
        """
        Processes the ListNotificationsByUserIdQuery.
        """
        notifications = await self.repository.list_by_user_id(
            query.user_id, query.limit, query.offset
        )
        total_count = await self.repository.count_by_user_id(query.user_id)

        return NotificationListResponse(
            notifications=[NotificationResponse(**n.to_dict()) for n in notifications],
            total_count=total_count,
        )


class ListNotificationsByStatusQueryHandler:
    """
    Handles the ListNotificationsByStatusQuery to retrieve notifications by status.
    """

    def __init__(self, repository: NotificationRepository):
        self.repository = repository

    async def handle(
        self, query: ListNotificationsByStatusQuery
    ) -> NotificationListResponse:
        """
        Processes the ListNotificationsByStatusQuery.
        """
        notifications = await self.repository.list_by_status(
            query.status, query.limit, query.offset
        )
        total_count = await self.repository.count_by_status(query.status)
        return NotificationListResponse(
            notifications=[NotificationResponse(**n.to_dict()) for n in notifications],
            total_count=total_count,
        )
