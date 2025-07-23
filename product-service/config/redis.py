from redis import asyncio as aioredis, Redis
import logging
from redis.asyncio.client import Redis

logger = logging.getLogger("app")
from config.app_config import settings
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import default_key_builder


class RedisManager:
    _instance = None
    _is_initialized = False

    @classmethod
    async def get_client(cls) -> Redis:
        if not cls._is_initialized:
            await cls.initialize()
        return cls._instance

    @classmethod
    async def initialize(cls):
        try:
            cls._instance = aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=False,
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True,
            )
            await cls._instance.ping()
            logger.info("Redis connection established")

            FastAPICache.init(
                RedisBackend(cls._instance),
                prefix="product-cache",
                expire=3600,
                key_builder=default_key_builder,
            )

            cls._is_initialized = True
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            raise

    @classmethod
    async def close(cls):
        if cls._instance:
            await cls._instance.close()
            cls._is_initialized = False
            cls._instance = None
            logger.info("Redis connection closed")


async def get_redis():
    return await RedisManager.get_client()
