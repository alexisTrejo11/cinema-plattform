from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH"

@dataclass
class Notification:
    user_id: str
    data: Dict[str, Any]
    notification_type: NotificationType
    created_at: datetime = datetime.now()