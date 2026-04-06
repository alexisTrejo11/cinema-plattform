"""Kafka topic placeholders for notification incoming integrations."""

from dataclasses import dataclass

from app.config.app_config import settings


@dataclass(frozen=True)
class NotificationTopicRegistry:
    incoming: str = settings.KAFKA_TOPIC_NOTIFICATION_INCOMING
    events: str = settings.KAFKA_TOPIC_NOTIFICATION_EVENTS
    dlq: str = settings.KAFKA_TOPIC_NOTIFICATION_DLQ


TOPICS = NotificationTopicRegistry()
