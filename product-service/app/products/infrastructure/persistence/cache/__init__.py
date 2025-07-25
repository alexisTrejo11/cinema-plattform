from .decorators import CacheDecorator
from fastapi_cache.backends.redis import RedisBackend

# Configuración inicial
redis_decorator = CacheDecorator()

cache = redis_decorator.cache
invalidate_cache = redis_decorator.invalidate_cache
