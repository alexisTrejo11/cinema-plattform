import redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry
from redis.exceptions import ConnectionError, TimeoutError
import time
import logging

logger = logging.getLogger(__name__)

retry = Retry(
    ExponentialBackoff(cap=10, base=1), 
    retries=5
)

def get_redis_client() -> redis.Redis:
    """
    Create and return a Redis client with basic robust connection handling.
    This version uses minimal parameters to avoid compatibility issues.
    """
    max_attempts = 3
    attempt = 0
    
    while attempt < max_attempts:
        try:
            attempt += 1
            logger.info(f"Attempting to connect to Redis (attempt {attempt}/{max_attempts})")
            
            client = redis.Redis(
                host='redis',
                port=6379,
                decode_responses=True,
                socket_connect_timeout=10,
                socket_timeout=10,
                health_check_interval=30
            )
            
            # Test the connection with a simple ping
            logger.info("Testing Redis connection with ping...")
            client.ping()
            logger.info("Successfully connected and pinged Redis.")
            return client
            
        except (ConnectionError, TimeoutError) as e:
            logger.error(f"Redis connection attempt {attempt} failed: {e}")
            if attempt < max_attempts:
                wait_time = 2 ** attempt  # Exponential backoff: 2, 4, 8 seconds
                logger.info(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                logger.error("All Redis connection attempts failed")
                raise ConnectionError(f"Failed to connect to Redis after {max_attempts} attempts: {e}")
        except Exception as e:
            logger.error(f"Unexpected error connecting to Redis: {e}")
            raise
