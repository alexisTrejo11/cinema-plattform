from typing import Any
import logging
import asyncio
from fastapi.exceptions import RequestValidationError
from app.shared.base_exceptions import (
    AuthorizationException,
    DomainException,
    ApplicationException,
)
from pydantic import ValidationError

from config.message.rabbit_consumer import RabbitMQConsumer
from config.app.app_config import settings
from config.db.redis import RedisManager, get_redis
from app.shared.redis.redis_service import RedisService

logger = logging.getLogger("app")

from .app.global_exception_handler import (
    handle_domain_exceptions,
    handle_application_exceptions,
    handle_generic_exceptions,
    handle_pydantic_validation_errors,
    handle_generic_exceptions,
    handle_path_validation_errors,
    handle_auth_exceptions,
    handle_value_errors,
)

exception_handlers: Any = {
    DomainException: handle_domain_exceptions,
    ApplicationException: handle_application_exceptions,
    Exception: handle_generic_exceptions,
    ValidationError: handle_pydantic_validation_errors,
    Exception: handle_generic_exceptions,
    RequestValidationError: handle_path_validation_errors,
    AuthorizationException: handle_auth_exceptions,
    ValueError: handle_value_errors,
}


async def init_rabbitmq():
    rabbitmq_consumer = RabbitMQConsumer(
        settings.RABBITMQ_URL,
        settings.USER_EVENTS_EXCHANGE,
        settings.CONSUMER_QUEUE_NAME,
    )
    await rabbitmq_consumer.connect()
    consumer_task = asyncio.create_task(rabbitmq_consumer.start_consuming())
    return consumer_task


async def close_rabbitmq(consumer_task):
    consumer_task.cancel()
    try:
        await asyncio.wait_for(consumer_task, timeout=5.0)
    except asyncio.CancelledError:
        logger.info("RabbitMQ consumer task cancelled successfully.")
    except Exception as e:
        logger.error(f"Error during consumer task cancellation: {e}")


async def init_redis():
    await RedisManager.initialize()
    client = await get_redis()
    await RedisService.initialize(client)
