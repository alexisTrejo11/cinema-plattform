"""JWT helpers for integration tests (same signing rules as access tokens)."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from app.config.app_config import settings
from app.shared.token.core import TokenType


def encode_access_token(*, user_id: int | str) -> str:
    """HS256 access token with `sub` = user id (matches get_logged_user)."""
    now = datetime.now(timezone.utc)
    exp = now + timedelta(hours=1)
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "type": TokenType.JWT_ACCESS.value,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    if settings.JWT_AUDIENCE:
        payload["aud"] = settings.JWT_AUDIENCE
    if settings.JWT_ISSUER:
        payload["iss"] = settings.JWT_ISSUER
    encoded = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded if isinstance(encoded, str) else encoded.decode("utf-8")


def bearer_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}
