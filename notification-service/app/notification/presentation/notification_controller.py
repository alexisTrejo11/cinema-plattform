from fastapi import APIRouter, HTTPException, Depends, Query, status
from uuid import UUID
from app.notification.application.dtos import (
    NotificationListResponse,
    NotificationResponse,
)
from app.notification.application.queries.notification_queries import (
    GetNotificationByIdQuery,
    ListNotificationsByChannelQuery,
    ListNotificationsByStatusQuery,
    ListNotificationsByTypeQuery,
    ListNotificationsByUserIdQuery,
)

from app.notification.application.queries.notification_query_handler import (
    GetNotificationByIdQueryHandler,
    ListNotificationsByChannelQueryHandler,
    ListNotificationsByStatusQueryHandler,
    ListNotificationsByTypeQueryHandler,
    ListNotificationsByUserIdQueryHandler,
)

from .dependencies import (
    get_get_notification_by_id_handler,
    get_list_notifications_by_type_handler,
    get_list_notifications_by_channel_handler,
    get_list_notifications_by_status_handler,
    get_list_notifications_by_user_id_handler,
)


router = APIRouter(prefix="/api/v2/notifications")


@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification_by_id(
    notification_id: UUID,
    handler: GetNotificationByIdQueryHandler = Depends(
        get_get_notification_by_id_handler
    ),
):
    """
    Retrieve a single notification by its unique ID.
    """
    query = GetNotificationByIdQuery(notification_id=notification_id)
    notification = await handler.handle(query)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found"
        )
    return notification


@router.get("/by-type/{notification_type}", response_model=NotificationListResponse)
async def list_notifications_by_type(
    notification_type: str,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    handler: ListNotificationsByTypeQueryHandler = Depends(
        get_list_notifications_by_type_handler
    ),
):
    """
    List notifications filtered by type.
    """
    query = ListNotificationsByTypeQuery(
        notification_type=notification_type, limit=limit, offset=offset
    )
    return await handler.handle(query)


@router.get("/by-channel/{channel}", response_model=NotificationListResponse)
async def list_notifications_by_channel(
    channel: str,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    handler: ListNotificationsByChannelQueryHandler = Depends(
        get_list_notifications_by_channel_handler
    ),
):
    """
    List notifications filtered by channel.
    """
    query = ListNotificationsByChannelQuery(channel=channel, limit=limit, offset=offset)
    return await handler.handle(query)


@router.get("/by-user/{user_id}", response_model=NotificationListResponse)
async def list_notifications_by_user_id(
    user_id: str,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    handler: ListNotificationsByUserIdQueryHandler = Depends(
        get_list_notifications_by_user_id_handler
    ),
):
    """
    List notifications for a specific user.
    """
    query = ListNotificationsByUserIdQuery(user_id=user_id, limit=limit, offset=offset)
    return await handler.handle(query)


@router.get("/by-status/{status}", response_model=NotificationListResponse)
async def list_notifications_by_status(
    status: str,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    handler: ListNotificationsByStatusQueryHandler = Depends(
        get_list_notifications_by_status_handler
    ),
):
    """
    List notifications filtered by status.
    """
    query = ListNotificationsByStatusQuery(status=status, limit=limit, offset=offset)
    return await handler.handle(query)
