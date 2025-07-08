from __future__ import annotations
from enum import Enum


class NotificationType(Enum):
    """
    Represents the type of notification.
    """

    PRODUCT_BUY = "PRODUCT_BUY"
    TICKET_BUY = "TICKET_BUY"
    ACCOUNT_CREATED = "ACCOUNT_CREATED"
    ACCOUNT_DELETED = "ACCOUNT_DELETED"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    ANNOUNCMENT = "ANNOUNCEMENT"
    CUSTOM_MESSAGE = "CUSTOM_MESSAGE"


class NotificationChannel(Enum):
    """
    Represents the communication channel for the notification.
    """

    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH_NOTIFICATION = "PUSH_NOTIFICATION"
    IN_APP = "IN_APP"


class NotificationStatus(Enum):
    """
    Represents the current status of the notification.
    """

    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"
    DELIVERED = "DELIVERED"
    READ = "READ"
    CANCELED = "CANCELED"
