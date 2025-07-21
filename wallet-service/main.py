from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI
import logging
from app.wallet.presentation.controllers import wallet_controller
from app.user.presentation import user_admin_controller
from config.app_config import settings
import asyncio
from config.global_exception_handler import GLOBAL_EXCEPTION_HANDLERS
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from config.logging import setup_logging
from config.queue.rabbit_consumer import RabbitMQConsumer
from middleware.logging_middleware import LoggingMiddleware
from config.register_server import RegistryMicroservice

logger = logging.getLogger("app")
limiter = Limiter(key_func=get_remote_address, default_limits=["30/minute"])
registry_client: Optional[RegistryMicroservice] = None

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Wallet Service...")

    # Registry Microservice registration
    registry_client = RegistryMicroservice()
    registered, instance_id = await registry_client.perfom_registry()

    if registered:
        logger.info(
            f"Wallet Service successfully registered with instance ID: {instance_id}"
        )
        await registry_client.start_heartbeat_loop()
    else:
        logger.error("Failed to register Wallet Service. Heartbeats will not be sent.")

    # Initialize RabbitMQ Consumer
    logger.info(f"Connecting to RabbitMQ....")
    rabbitmq_consumer = RabbitMQConsumer(
        settings.RABBITMQ_URL,
        settings.USER_EVENTS_EXCHANGE,
        settings.CONSUMER_QUEUE_NAME,
    )
    await rabbitmq_consumer.connect()
    # app.state.rabbitmq_consumer = rabbitmq_consumer
    consumer_task = asyncio.create_task(rabbitmq_consumer.start_consuming())
    logger.info("RabbitMQ consumer background task started.")

    # Start Server
    yield

    # Shutdown process
    logger.info("Shutting down Wallet Service...")
    if registry_client:
        registry_client.stop_heartbeat_loop()
        logger.info("Heartbeat loop stopped.")

    logger.info(
        "Application shutdown: Closing RabbitMQ consumer and database connections..."
    )

    # if app.state.consumer_task:
    if consumer_task:
        consumer_task.cancel()
        try:
            await asyncio.wait_for(consumer_task, timeout=5.0)
        except asyncio.CancelledError:
            logger.info("RabbitMQ consumer task cancelled successfully.")
        except Exception as e:
            logger.error(f"Error during consumer task cancellation: {e}")

    if rabbitmq_consumer:
        await rabbitmq_consumer.close()
        logger.info("RabbitMQ connection closed.")


app = FastAPI(
    title="Wallet Service API",
    description="API for managing wallets and users.",
    version="1.0.0",
    exception_handlers=GLOBAL_EXCEPTION_HANDLERS,
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_middleware(LoggingMiddleware)
app.add_middleware(SlowAPIMiddleware)


@app.get("/")
async def read_root():
    return {"message": "Wallet Service is running and listening for user events!"}


@app.get("/health")
async def read_health():
    return {"status": "healthy", "service": "wallet-service"}


app.include_router(wallet_controller.router)
app.include_router(user_admin_controller.router)
