import json
from typing import Any, AsyncIterator, List, Optional
from redis import Redis
from .serializer import SerializerService


class RedisService:
    _client: Optional[Redis] = None

    @classmethod
    async def initialize(cls, client: Redis):
        cls._client = client

    @classmethod
    async def get_client(cls) -> Redis:
        if cls._client is None:
            raise RuntimeError("RedisService not initialized")
        return cls._client

    @classmethod
    async def get(cls, key: str) -> Optional[Any]:
        client = await cls.get_client()
        value = await client.get(key)
        return json.loads(value) if value else None

    @classmethod
    async def get_many(
        cls, keys: List[str]
    ) -> AsyncIterator[tuple[str, Optional[Any]]]:
        """Obtiene múltiples valores eficientemente"""
        client = await cls.get_client()
        values = await client.mget(keys)
        for key, value in zip(keys, values):
            yield key, json.loads(value) if value else None

    @classmethod
    async def delete(cls, key: str) -> int:
        """Elimina una clave específica"""
        client = await cls.get_client()
        return await client.delete(key)

    @classmethod
    async def delete_pattern(cls, pattern: str) -> int:
        """Elimina todas las claves que coincidan con un patrón"""
        client = await cls.get_client()
        keys = []
        for key in client.scan_iter(match=pattern):
            keys.append(key)
        if keys:
            return await client.delete(*keys)
        return 0

    @classmethod
    async def save(cls, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Guarda un valor en Redis con una clave específica"""
        client = await cls.get_client()

        serialized = SerializerService.serialize(value)
        value_str = json.dumps(serialized)
        if expire:
            return await client.set(key, value_str, ex=expire)
        return await client.set(key, value_str)

    @classmethod
    async def delete_namespace(cls, namespace: str) -> int:
        """Elimina todas las claves de un namespace (ej: 'product:*')"""
        return await cls.delete_pattern(f"{namespace}:*")
