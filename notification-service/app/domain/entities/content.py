from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass(frozen=True)
class NotificationContent:
    """
    Value object representing the content of a notification.
    """

    subject: str
    body: str
    template_name: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """
        Validates content presence.
        """
        if not self.subject or not self.body:
            raise ValueError("Notification content must have a subject and a body.")
