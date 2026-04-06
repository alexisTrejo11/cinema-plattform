from typing import Any, Dict, List, Optional
import logging

from pymongo.results import InsertOneResult

from app.notification.domain.entities.models import Notification
from app.notification.domain.enums import (
    NotificationAttentionStatus,
    NotificationChannel,
    NotificationStatus,
    NotificationType,
)
from app.notification.domain.repository import NotificationRepository

logger = logging.getLogger("app")


class MongoNotificationRepository(NotificationRepository):
    def __init__(self, database) -> None:
        self.collection = database["notifications"]

    async def get_by_id(self, notification_id: str) -> Optional[Notification]:
        try:
            document = await self.collection.find_one({"_id": notification_id})
            if document is None:
                return None
            return Notification.from_document(document)
        except Exception:
            logger.exception("repository.get_by_id failed notification_id=%s", notification_id)
            raise

    async def list_notifications(
        self,
        *,
        notification_type: Optional[NotificationType] = None,
        channel: Optional[NotificationChannel] = None,
        user_id: Optional[str] = None,
        status: Optional[NotificationStatus] = None,
        is_important: Optional[bool] = None,
        attention_status: Optional[NotificationAttentionStatus] = None,
        source_event_type: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> List[Notification]:
        query = self._build_query(
            notification_type=notification_type,
            channel=channel,
            user_id=user_id,
            status=status,
            is_important=is_important,
            attention_status=attention_status,
            source_event_type=source_event_type,
        )
        try:
            cursor = (
                self.collection.find(query).sort("created_at", -1).skip(offset).limit(limit)
            )
            docs = await cursor.to_list(length=limit)
            return [Notification.from_document(doc) for doc in docs]
        except Exception:
            logger.exception("repository.list_notifications failed")
            raise

    async def count_notifications(
        self,
        *,
        notification_type: Optional[NotificationType] = None,
        channel: Optional[NotificationChannel] = None,
        user_id: Optional[str] = None,
        status: Optional[NotificationStatus] = None,
        is_important: Optional[bool] = None,
        attention_status: Optional[NotificationAttentionStatus] = None,
        source_event_type: Optional[str] = None,
    ) -> int:
        query = self._build_query(
            notification_type=notification_type,
            channel=channel,
            user_id=user_id,
            status=status,
            is_important=is_important,
            attention_status=attention_status,
            source_event_type=source_event_type,
        )
        try:
            return await self.collection.count_documents(query)
        except Exception:
            logger.exception("repository.count_notifications failed")
            raise

    async def save(self, notification: Notification) -> Notification:
        try:
            result: InsertOneResult = await self.collection.insert_one(
                notification.to_document()
            )
            if not result.acknowledged:
                raise RuntimeError("Failed to persist notification")
            return notification
        except Exception:
            logger.exception(
                "repository.save failed notification_id=%s", notification.notification_id
            )
            raise

    async def update(self, notification: Notification) -> Notification:
        try:
            result = await self.collection.replace_one(
                {"_id": notification.notification_id},
                notification.to_document(),
            )
            if result.matched_count == 0:
                raise RuntimeError(
                    f"Notification {notification.notification_id} not found for update."
                )
            return notification
        except Exception:
            logger.exception(
                "repository.update failed notification_id=%s", notification.notification_id
            )
            raise

    async def get_by_event_id(self, event_id: str) -> Optional[Notification]:
        try:
            document = await self.collection.find_one({"event_id": event_id})
            if document is None:
                return None
            return Notification.from_document(document)
        except Exception:
            logger.exception("repository.get_by_event_id failed event_id=%s", event_id)
            raise

    def _build_query(
        self,
        *,
        notification_type: Optional[NotificationType],
        channel: Optional[NotificationChannel],
        user_id: Optional[str],
        status: Optional[NotificationStatus],
        is_important: Optional[bool],
        attention_status: Optional[NotificationAttentionStatus],
        source_event_type: Optional[str],
    ) -> Dict[str, Any]:
        query: Dict[str, Any] = {}
        if notification_type is not None:
            query["notification_type"] = notification_type.value
        if channel is not None:
            query["channel"] = channel.value
        if user_id:
            query["recipient.user_id"] = user_id
        if status is not None:
            query["status"] = status.value
        if is_important is not None:
            query["is_important"] = is_important
        if attention_status is not None:
            query["attention_status"] = attention_status.value
        if source_event_type:
            query["source_event_type"] = source_event_type
        return query
