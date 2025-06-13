import redis
from redis.cache import CacheConfig
from redis.backoff import ExponentialBackoff
from redis.retry import Retry

retry = Retry(ExponentialBackoff(), 3)

redisConn = redis.Redis(
    host='redis', 
    port=6379, 
    cache_config=CacheConfig(),
    password='redis_password_placeholder',
    decode_responses=True,
    retry=retry,
    retry_on_error=[ConnectionError],
    health_check_interval=30
    )
