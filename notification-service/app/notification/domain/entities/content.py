from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict


class NotificationContent(BaseModel):
    """Notification body value object."""

    model_config = ConfigDict(extra="allow")

    subject: str
    body: str
    template_name: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
