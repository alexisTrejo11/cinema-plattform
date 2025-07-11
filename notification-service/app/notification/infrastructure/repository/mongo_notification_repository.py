from typing import Optional, Dict, Any, List
from app.notification.domain.entities.models import (
    Notification,
    NotificationType,
    NotificationChannel,
    NotificationStatus,
    Recipient,
    NotificationContent,
)
from app.notification.domain.repository import NotificationRepository
from uuid import UUID
from datetime import datetime
import logging
from pymongo.results import InsertOneResult

logger = logging.getLogger("app")


class MongoNotificationRepository(NotificationRepository):
    def __init__(self, database) -> None:
        self.collection = database["notifications"]

    async def get_by_id(self, notification_id: UUID) -> Optional[Notification]:
        """Obtiene una notificación por su ID"""
        try:
            doc = await self.collection.find_one({"_id": str(notification_id)})
            if not doc:
                return None
            return self._to_entity(doc)
        except Exception as e:
            logger.error(f"Error getting notification by ID {notification_id}: {e}")
            raise

    async def list_by_type(
        self, notification_type: str, limit: int, offset: int
    ) -> List[Notification]:
        """Lista notificaciones por tipo"""
        try:
            cursor = self.collection.find({"notification_type": notification_type})
            return await self._cursor_to_entities(cursor, limit, offset)
        except Exception as e:
            logger.error(
                f"Error listing notifications by type {notification_type}: {e}"
            )
            raise

    async def list_by_channel(
        self, channel: str, limit: int, offset: int
    ) -> List[Notification]:
        """Lista notificaciones por canal"""
        try:
            cursor = self.collection.find({"channel": channel})
            return await self._cursor_to_entities(cursor, limit, offset)
        except Exception as e:
            logger.error(f"Error listing notifications by channel {channel}: {e}")
            raise

    async def list_by_user_id(
        self, user_id: UUID, limit: int, offset: int
    ) -> List[Notification]:
        """Lista notificaciones por ID de usuario"""
        try:
            cursor = self.collection.find({"recipient.user_id": str(user_id)})
            return await self._cursor_to_entities(cursor, limit, offset)
        except Exception as e:
            logger.error(f"Error listing notifications by user ID {user_id}: {e}")
            raise

    async def list_by_status(
        self, status: str, limit: int, offset: int
    ) -> List[Notification]:
        """Lista notificaciones por estado"""
        try:
            cursor = self.collection.find({"status": status})
            return await self._cursor_to_entities(cursor, limit, offset)
        except Exception as e:
            logger.error(f"Error listing notifications by status {status}: {e}")
            raise

    async def count_by_type(self, notification_type: str) -> int:
        """Cuenta notificaciones por tipo"""
        return await self.collection.count_documents(
            {"notification_type": notification_type}
        )

    async def count_by_channel(self, channel: str) -> int:
        """Cuenta notificaciones por canal"""
        return await self.collection.count_documents({"channel": channel})

    async def count_by_user_id(self, user_id: UUID) -> int:
        """Cuenta notificaciones por ID de usuario"""
        return await self.collection.count_documents(
            {"recipient.user_id": str(user_id)}
        )

    async def count_by_status(self, status: str) -> int:
        """Cuenta notificaciones por estado"""
        return await self.collection.count_documents({"status": status})

    async def save(self, notification: Notification) -> Notification:
        """Guarda una notificación"""
        try:
            doc = self._to_document(notification)
            result: InsertOneResult = await self.collection.insert_one(doc)
            if not result.acknowledged:
                raise Exception("Failed to save notification")

            # Retornamos la entidad con el ID generado
            notification.set_notification_id(str(UUID(result.inserted_id)))
            return notification
        except Exception as e:
            logger.error(f"Error saving notification: {e}")
            raise

    async def _cursor_to_entities(
        self, cursor, limit: int, offset: int
    ) -> List[Notification]:
        """Convierte un cursor de MongoDB a una lista de entidades"""
        try:
            docs = await cursor.skip(offset).limit(limit).to_list(length=limit)
            return [self._to_entity(doc) for doc in docs]
        except Exception as e:
            logger.error(f"Error converting cursor to entities: {e}")
            raise

    def _to_entity(self, doc: Dict[str, Any]) -> Notification:
        """Convierte un documento de MongoDB a una entidad Notification"""
        try:
            transformed = self._transform_document(doc)
            return Notification(**transformed)
        except Exception as e:
            logger.error(f"Error transforming document to entity: {e}")
            raise

    def _to_document(self, notification: Notification) -> Dict[str, Any]:
        """Convierte una entidad Notification a un documento de MongoDB"""
        try:
            doc = notification.to_dict()
            doc["_id"] = str(doc.pop("notification_id"))

            # Convertir enums a strings
            doc["notification_type"] = doc["notification_type"].value
            doc["channel"] = doc["channel"].value
            doc["status"] = doc["status"].value

            # Convertir objetos value a dicts
            doc["recipient"] = doc["recipient"].dict()
            doc["content"] = doc["content"].dict()

            return doc
        except Exception as e:
            logger.error(f"Error transforming entity to document: {e}")
            raise

    def _transform_document(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Transforma el documento de MongoDB al formato esperado por el dominio"""
        try:
            transformed = doc.copy()

            # ID conversion
            transformed["notification_id"] = str(transformed.pop("_id"))

            # Enum conversions
            enum_fields = {
                "notification_type": NotificationType,
                "channel": NotificationChannel,
                "status": NotificationStatus,
            }

            for field, enum_class in enum_fields.items():
                if field in transformed:
                    transformed[field] = enum_class(transformed[field])

            # Date conversions
            date_fields = ["created_at", "sent_at", "failed_at"]
            for field in date_fields:
                if field in transformed and transformed[field]:
                    if isinstance(transformed[field], str):
                        transformed[field] = datetime.fromisoformat(transformed[field])
                    elif not isinstance(transformed[field], datetime):
                        logger.warning(f"Unexpected date format for field {field}")
                        transformed[field] = None

            # Value objects
            if "recipient" in transformed:
                transformed["recipient"] = Recipient(**transformed["recipient"])

            if "content" in transformed:
                transformed["content"] = NotificationContent(**transformed["content"])

            return transformed
        except Exception as e:
            logger.error(f"Error transforming document: {e}")
            raise
