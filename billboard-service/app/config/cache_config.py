import logging
from redis import asyncio as redis
from typing import Optional, Any
import json

from fastapi_cache import caches
from fastapi_cache.backends.redis import RedisCacheBackend

from app.config.app_config import settings



logger = logging.getLogger(__name__)
FastAPICache = caches 

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

# Global cache service instance
cache_service: Optional[CacheService] = None
redis_client: Optional[Any] = None


async def init_cache(redis_url: str = settings.redis_url):
    """
    Initialize Redis cache and the fastapi_cache registry.
    If anything fails, the application continues without caching.
    """
    global cache_service, redis_client

    try:
        # Create a low-level Redis client for our own CacheService helpers
        if redis is not None:
            redis_client = redis.from_url(redis_url, encoding="utf8", decode_responses=True)

            # Simple connectivity check
            await redis_client.ping()

            cache_service = CacheService(redis_client)

        # Register fastapi-cache backend (used by @cache decorator if you use it)
        caches.set("default", RedisCacheBackend(redis_url))

        logger.info("Redis cache initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Redis cache: {e}")
        logger.warning("Application will continue without caching")
        cache_service = None
        redis_client = None


async def close_cache() -> None:
    """Close Redis connection properly"""
    global redis_client
    if redis_client:
        await redis_client.close()
        logger.info("Redis connection closed")

def get_redis_client():
    """Get Redis client for direct usage"""
    return redis_client