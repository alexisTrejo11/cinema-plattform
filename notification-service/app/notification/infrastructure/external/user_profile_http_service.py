from __future__ import annotations

import logging

import httpx

from app.config.app_config import settings
from app.notification.domain.user_profile_service import (
    UserContactProfile,
    UserProfileService,
)

logger = logging.getLogger("app")


class HttpUserProfileService(UserProfileService):
    """Best-effort user-contact lookup from user-service HTTP endpoints."""

    async def resolve_contact(self, user_id: str) -> UserContactProfile | None:
        if not settings.USER_DIRECTORY_LOOKUP_ENABLED:
            return None

        timeout = httpx.Timeout(settings.USER_DIRECTORY_TIMEOUT_SECONDS)
        base_url = settings.USER_DIRECTORY_BASE_URL.rstrip("/")
        candidate_paths = [
            f"/api/v2/users/{user_id}",
            f"/api/v1/users/{user_id}",
            f"/users/{user_id}",
        ]

        async with httpx.AsyncClient(timeout=timeout) as client:
            for path in candidate_paths:
                try:
                    response = await client.get(f"{base_url}{path}")
                    if response.status_code != 200:
                        continue
                    payload = response.json()
                    data = payload.get("data", payload)
                    email = data.get("email")
                    phone_number = data.get("phone_number") or data.get("phone")
                    if not email and not phone_number:
                        continue
                    return UserContactProfile(
                        user_id=str(data.get("id", user_id)),
                        email=email,
                        phone_number=phone_number,
                    )
                except Exception:
                    logger.debug(
                        "user_directory.lookup_failed user_id=%s path=%s",
                        user_id,
                        path,
                        exc_info=True,
                    )
        return None
