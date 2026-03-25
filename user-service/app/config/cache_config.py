import json
import logging
from typing import Any, Optional

from fastapi_cache import caches
from fastapi_cache.backends.redis import RedisCacheBackend
from redis import asyncio as redis

from app.config.app_config import settings

logger = logging.getLogger(__name__)
FastAPICache = caches

_STARTUP_CHECK_KEY = "__user_service:redis_startup_check__"


class CacheService:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def get(self, key: str) -> Optional[Any]:
        data = await self.redis.get(key)
        return json.loads(data) if data else None

    async def set(self, key: str, value: Any, expire: int = 60):
        await self.redis.setex(key, expire, json.dumps(value, default=str))

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def delete_pattern(self, pattern: str):
        """Delete all keys that match a pattern"""
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)


cache_service: Optional[CacheService] = None
redis_client: Optional[Any] = None


async def _verify_redis_read_write(client) -> None:
    """Ping alone is not enough; confirm SET/GET works with decode_responses."""
    await client.set(_STARTUP_CHECK_KEY, "ok", ex=10)
    val = await client.get(_STARTUP_CHECK_KEY)
    if val != "ok":
        raise RuntimeError(
            f"Redis read/write check failed: expected 'ok', got {val!r}"
        )
    await client.delete(_STARTUP_CHECK_KEY)


async def init_cache(redis_url: str | None = None) -> None:
    """
    Initialize Redis client, fastapi-cache backend, and CacheService.

    When REDIS_VALIDATE_ON_STARTUP is True (default), any failure aborts startup
    (caller should treat raised exception as fatal).

    When False (e.g. tests without Redis), failures are logged and cache globals stay None.
    """
    global cache_service, redis_client

    url = redis_url or settings.REDIS_URL
    strict = settings.REDIS_VALIDATE_ON_STARTUP

    try:
        redis_client = redis.from_url(
            url, encoding="utf8", decode_responses=True
        )
        await redis_client.ping()
        await _verify_redis_read_write(redis_client)

        cache_service = CacheService(redis_client)
        caches.set("default", RedisCacheBackend(url))

        logger.info("Redis cache initialized successfully (ping + read/write OK).")
    except Exception as e:
        cache_service = None
        redis_client = None
        if strict:
            logger.critical(
                "Redis startup validation failed; refusing to initialize cache. %s",
                e,
                exc_info=True,
            )
            raise RuntimeError(f"Redis unavailable: {e}") from e
        logger.error("Failed to initialize Redis cache: %s", e)
        logger.warning("Application will continue without caching")


async def close_cache() -> None:
    """Close Redis connection properly"""
    global redis_client
    if redis_client:
        await redis_client.close()
        logger.info("Redis connection closed")


def get_redis_client():
    """Get Redis client for direct usage"""
    return redis_client
