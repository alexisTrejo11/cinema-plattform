"""Redis-backed async cache used by domain cache decorators."""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any, Optional

from app.config.app_config import settings

if TYPE_CHECKING:
    from redis.asyncio import Redis

logger = logging.getLogger("app")

_redis: Optional["Redis"] = None
cache_service: Optional["CacheService"] = None


class CacheService:
    """JSON-serialised values in Redis (decode_responses=True on the client)."""

    async def get(self, key: str) -> Any | None:
        client = get_redis_client()
        if client is None:
            return None
        raw = await client.get(key)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            logger.warning("Invalid JSON in cache for key %s; dropping entry.", key)
            await client.delete(key)
            return None

    async def set(self, key: str, value: Any, *, expire: int = 300) -> None:
        client = get_redis_client()
        if client is None:
            return
        payload = json.dumps(value, default=str)
        await client.set(key, payload, ex=expire)

    async def delete_pattern(self, pattern: str) -> None:
        client = get_redis_client()
        if client is None:
            return
        async for k in client.scan_iter(match=pattern, count=200):
            await client.delete(k)


async def init_cache() -> None:
    global _redis, cache_service
    cache_service = None
    if _redis is not None:
        try:
            await _redis.close()
        except Exception:
            pass
        _redis = None

    try:
        from redis.asyncio import Redis

        _redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
        if settings.REDIS_VALIDATE_ON_STARTUP:
            await _redis.ping()
        cache_service = CacheService()
        logger.info("Redis cache initialized.")
    except Exception as exc:
        logger.warning("Redis unavailable (%s); continuing without cache.", exc)
        if _redis is not None:
            try:
                await _redis.close()
            except Exception:
                pass
        _redis = None
        cache_service = None


async def close_cache() -> None:
    global _redis, cache_service
    cache_service = None
    if _redis is not None:
        try:
            close = getattr(_redis, "aclose", None)
            if callable(close):
                await close()
            else:
                await _redis.close()
        except Exception as exc:
            logger.debug("Redis close: %s", exc)
        _redis = None


def get_redis_client() -> Optional["Redis"]:
    return _redis
