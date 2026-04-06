import redis.asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.config.app_config import settings

_redis_client: aioredis.Redis | None = None


async def init_cache() -> None:
    global _redis_client
    _redis_client = aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    FastAPICache.init(RedisBackend(_redis_client), prefix="employee-service:")


async def close_cache() -> None:
    global _redis_client
    if _redis_client:
        await _redis_client.aclose()
        _redis_client = None


def get_redis_client() -> aioredis.Redis:
    if _redis_client is None:
        raise RuntimeError("Cache not initialised — call init_cache() first")
    return _redis_client
