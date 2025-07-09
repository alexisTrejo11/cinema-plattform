from typing import Optional, Dict, Any, List
from app.domain.entities.models import Notification
from app.domain.repository import NotificationRepository
from uuid import UUID


class MongoNotificationRepository(NotificationRepository):
    def __init__(self, database) -> None:
        self.collection = database["notification"]

    async def get_by_id(self, notification_id: UUID) -> Optional[Notification]:
        doc = await self.collection.find_one({"_id", notification_id})
        if not doc:
            return None

        doc["notification_id"] = doc.pop("_id")
        return Notification(**doc)

    async def list_by_type(
        self, notification_type: str, limit: int, offset: int
    ) -> List[Notification]:
        cursor = (
            self.collection.find({"type": notification_type}).skip(offset).limit(limit)
        )
        return [
            Notification(**(doc | {"notification_id": doc.pop("_id")}))
            for doc in await cursor.to_list(length=limit)
        ]

    async def list_by_channel(
        self, channel: str, limit: int, offset: int
    ) -> List[Notification]:
        cursor = self.collection.find({"channel": channel}).skip(offset).limit(limit)
        return [
            Notification(**(doc | {"notification_id": doc.pop("_id")}))
            for doc in await cursor.to_list(length=limit)
        ]

    async def list_by_user_id(
        self, user_id: UUID, limit: int, offset: int
    ) -> List[Notification]:
        cursor = self.collection.find({"user_id": user_id}).skip(offset).limit(limit)
        return [
            Notification(**(doc | {"notification_id": doc.pop("_id")}))
            for doc in await cursor.to_list(length=limit)
        ]

    async def list_by_status(
        self, status: str, limit: int, offset: int
    ) -> List[Notification]:
        cursor = self.collection.find({"status": status}).skip(offset).limit(limit)
        return [
            Notification(**(doc | {"notification_id": doc.pop("_id")}))
            for doc in await cursor.to_list(length=limit)
        ]

    async def count_by_type(self, notification_type: str) -> int:
        return await self.collection.count_documents({"type": notification_type})

    async def count_by_channel(self, channel: str) -> int:
        return await self.collection.count_documents({"channel": channel})

    async def count_by_user_id(self, user_id: UUID) -> int:
        return await self.collection.count_documents({"user_id": user_id})

    async def count_by_status(self, status: str) -> int:
        return await self.collection.count_documents({"status": status})

    async def save(self, notification: Notification) -> None:
        doc = notification.to_dict()
        await self.collection.insert_one(doc)
