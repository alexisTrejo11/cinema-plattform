from typing import Optional, Dict, Any, List
from app.domain.entities.models import Notification
from app.domain.repository import NotificationRepository


# TODO: _id?? test
class MongoNotificationRepository(NotificationRepository):
    def __init__(self, mongo_db) -> None:
        self.collection = mongo_db["notification"]

    async def get_by_id(self, id: str) -> Optional[Notification]:
        doc = await self.collection.find_one({"_id", id})
        return Notification.from_dict(doc) if doc else None

    async def list_by_type(self, type: str) -> List[Notification]:
        notifications = []
        async for doc in self.collection.find({"type": type}):
            notifications.append(Notification.from_dict(doc))
        return notifications

    async def list_by_channel(self, channel: str) -> List[Notification]:
        notifications = []
        async for doc in self.collection.find({"channel": channel}):
            notifications.append(Notification.from_dict(doc))
        return notifications

    async def list_by_user_id(self, user_id: str) -> List[Notification]:
        notifications = []
        async for doc in self.collection.find({"user_id": user_id}):
            notifications.append(Notification.from_dict(doc))
        return notifications

    async def list_by_status(self, status: str) -> List[Notification]:
        notifications = []
        async for doc in self.collection.find({"status": status}):
            notifications.append(Notification.from_dict(doc))
        return notifications

    async def create(self, notification: Notification) -> None:
        doc = notification.to_dict()
        await self.collection.insert_one(doc)
