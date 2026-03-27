"""Redis client helpers for caching (optional)."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

from app.config.app_config import settings

if TYPE_CHECKING:
    from redis.asyncio import Redis

logger = logging.getLogger(__name__)

_redis: Optional["Redis"] = None


async def init_cache() -> None:
    global _redis
    if not settings.REDIS_VALIDATE_ON_STARTUP:
        return
    try:
        from redis.asyncio import Redis

        _redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
        await _redis.ping()
        logger.info("Redis cache initialized.")
    except Exception as exc:
        logger.warning("Redis unavailable (%s); continuing without cache.", exc)
        _redis = None


async def close_cache() -> None:
    global _redis
    if _redis is not None:
        await _redis.close()
        _redis = None


def get_redis_client() -> Optional["Redis"]:
    return _redis
