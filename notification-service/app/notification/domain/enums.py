from __future__ import annotations

from enum import Enum


class NotificationType(str, Enum):
    """
    Represents the type of notification.
    """

    PRODUCT_BUY = "PRODUCT_BUY"
    TICKET_BUY = "TICKET_BUY"
    ACCOUNT_AUTH = "ACCOUNT_AUTH"
    ACCOUNT_CREATED = "ACCOUNT_CREATED"
    ACCOUNT_DELETED = "ACCOUNT_DELETED"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    ANNOUNCEMENT = "ANNOUNCEMENT"
    CUSTOM_MESSAGE = "CUSTOM_MESSAGE"


class NotificationChannel(str, Enum):
    """
    Represents the communication channel for the notification.
    """

    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH_NOTIFICATION = "PUSH_NOTIFICATION"
    IN_APP = "IN_APP"


class NotificationStatus(str, Enum):
    """
    Represents the current status of the notification.
    """

    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"
    DELIVERED = "DELIVERED"
    READ = "READ"
    CANCELED = "CANCELED"


class NotificationAttentionStatus(str, Enum):
    """
    Monitoring state for alerts that need operational follow-up.
    """

    NONE = "NONE"
    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"
