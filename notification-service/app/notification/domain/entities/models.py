from __future__ import annotations
from datetime import datetime
from typing import Any, Optional, Dict
from ..enums import *
from .content import NotificationContent
from .recipient import Recipient


class Notification:
    """
    Domain class representing a notification.
    """

    def __init__(
        self,
        notification_id: str,
        notification_type: NotificationType,
        recipient: Recipient,
        content: NotificationContent,
        channel: NotificationChannel,
        created_at: datetime,
        event_id: Optional[str] = None,
        status: NotificationStatus = NotificationStatus.PENDING,
        sent_at: Optional[datetime] = None,
        failed_at: Optional[datetime] = None,
        error_details: Optional[str] = None,
        provider_response: Optional[str] = None,
    ):
        """
        Initializes a Notification domain object.
        """
        if not isinstance(notification_type, NotificationType):
            raise TypeError(
                "notification_type must be an instance of NotificationType Enum."
            )
        if not isinstance(recipient, Recipient):
            raise TypeError("recipient must be an instance of Recipient Value Object.")
        if not isinstance(content, NotificationContent):
            raise TypeError(
                "content must be an instance of NotificationContent Value Object."
            )
        if not isinstance(channel, NotificationChannel):
            raise TypeError("channel must be an instance of NotificationChannel Enum.")
        if not isinstance(created_at, datetime):
            raise TypeError("created_at must be a datetime object.")
        if not isinstance(status, NotificationStatus):
            raise TypeError("status must be an instance of NotificationStatus Enum.")

        self._notification_id = notification_id
        self._notification_type = notification_type
        self._recipient = recipient
        self._content = content
        self._channel = channel
        self._created_at = created_at
        self._event_id = event_id
        self._status = status
        self._sent_at = sent_at
        self._failed_at = failed_at
        self._error_details = error_details
        self._provider_response = provider_response

    @property
    def notification_id(self) -> str:
        """
        Returns the unique identifier of the notification.
        """
        return self._notification_id

    def set_notification_id(self, id: str) -> None:
        """
        Returns the unique identifier of the notification.
        """
        self._notification_id = id

    @property
    def notification_type(self) -> NotificationType:
        """
        Returns the type of the notification.
        """
        return self._notification_type

    @property
    def recipient(self) -> Recipient:
        """
        Returns the recipient of the notification.
        """
        return self._recipient

    @property
    def content(self) -> NotificationContent:
        """
        Returns the content of the notification.
        """
        return self._content

    @property
    def channel(self) -> NotificationChannel:
        """
        Returns the channel through which the notification will be sent.
        """
        return self._channel

    @property
    def created_at(self) -> datetime:
        """
        Returns the creation timestamp of the notification.
        """
        return self._created_at

    @property
    def event_id(self) -> Optional[str]:
        """
        Returns the ID of the external event that triggered this notification.
        """
        return self._event_id

    @property
    def status(self) -> NotificationStatus:
        """
        Returns the current status of the notification.
        """
        return self._status

    @property
    def sent_at(self) -> Optional[datetime]:
        """
        Returns the timestamp when the notification was successfully sent.
        """
        return self._sent_at

    @property
    def failed_at(self) -> Optional[datetime]:
        """
        Returns the timestamp when the notification sending failed.
        """
        return self._failed_at

    @property
    def error_details(self) -> Optional[str]:
        """
        Returns details about the error if sending failed.
        """
        return self._error_details

    @property
    def provider_response(self) -> Optional[str]:
        """
        Returns the raw response from the notification provider.
        """
        return self._provider_response

    def mark_as_sent(self, sent_at: Optional[datetime] = None) -> None:
        """
        Marks the notification status as SENT.
        """
        if self._status == NotificationStatus.FAILED:
            raise ValueError(
                "Cannot mark a failed notification as sent without re-processing."
            )
        self._status = NotificationStatus.SENT
        self._sent_at = sent_at if sent_at else datetime.now()
        self._failed_at = None
        self._error_details = None
        self._provider_response = None

    def mark_as_failed(
        self,
        error_details: str,
        failed_at: Optional[datetime] = None,
        provider_response: Optional[str] = None,
    ) -> None:
        """
        Marks the notification status as FAILED with error details.
        """
        self._status = NotificationStatus.FAILED
        self._failed_at = failed_at if failed_at else datetime.now()
        self._error_details = error_details
        self._provider_response = provider_response
        self._sent_at = None

    def mark_as_delivered(self) -> None:
        """
        Marks the notification status as DELIVERED.
        """
        if self._status != NotificationStatus.SENT:
            raise ValueError(
                "Notification must be in SENT status to be marked as DELIVERED."
            )
        self._status = NotificationStatus.DELIVERED

    def mark_as_read(self) -> None:
        """
        Marks the notification status as READ.
        """
        if self._status not in [
            NotificationStatus.SENT,
            NotificationStatus.DELIVERED,
        ]:
            raise ValueError(
                "Notification must be sent or delivered to be marked as READ."
            )
        self._status = NotificationStatus.READ

    def mark_as_pending(self) -> None:
        """
        Resets the notification status to PENDING for re-processing.
        """
        self._status = NotificationStatus.PENDING
        self._sent_at = None
        self._failed_at = None
        self._error_details = None
        self._provider_response = None

    def is_pending(self) -> bool:
        """
        Checks if the notification is in PENDING status.
        """
        return self._status == NotificationStatus.PENDING

    def is_sent(self) -> bool:
        """
        Checks if the notification is in SENT status.
        """
        return self._status == NotificationStatus.SENT

    def is_failed(self) -> bool:
        """
        Checks if the notification is in FAILED status.
        """
        return self._status == NotificationStatus.FAILED

    def __eq__(self, other: Any) -> bool:
        """
        Equality comparison based on notification_id.
        """
        if not isinstance(other, Notification):
            return NotImplemented
        return self.notification_id == other.notification_id

    def __hash__(self) -> int:
        """
        Hash based on notification_id for set/dict usage.
        """
        return hash(self.notification_id)

    def to_dict(self) -> dict:
        """
        Converts the Notification object to a dictionary representation.
        """
        return {
            "notification_id": self.notification_id,
            "notification_type": self.notification_type.value,
            "recipient": self.recipient.to_dict(),
            "content": self.content.to_dict(),
            "channel": self.channel.value,
            "created_at": self.created_at.isoformat(),
            "event_id": self.event_id,
            "status": self.status.value,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "failed_at": self.failed_at.isoformat() if self.failed_at else None,
            "error_details": self.error_details,
            "provider_response": self.provider_response,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Notification:
        """
        Creates a Notification object from a dictionary representation.
        """
        return Notification(
            notification_id=data["_id"],
            notification_type=NotificationType(data["notification_type"]),
            recipient=Recipient(**data["recipient"]),
            content=NotificationContent(**data["content"]),
            channel=NotificationChannel(data["channel"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            event_id=data.get("event_id"),
            status=NotificationStatus(data["status"]),
            sent_at=(
                datetime.fromisoformat(data["sent_at"]) if data.get("sent_at") else None
            ),
            failed_at=(
                datetime.fromisoformat(data["failed_at"])
                if data.get("failed_at")
                else None
            ),
            error_details=data.get("error_details"),
            provider_response=data.get("provider_response"),
        )
