from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime
from enum import Enum
from app.users.domain.entities import User

class NotificationType(str, Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH"

@dataclass
class Notification:
    user: User
    token: str
    notification_type: NotificationType
    created_at: datetime = datetime.now()