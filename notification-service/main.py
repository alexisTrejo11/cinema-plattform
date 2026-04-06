import asyncio
import logging
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware

from app.config.app_config import settings
from app.config.rate_limit import limiter
from app.config.global_exception_handler import GLOBAL_EXCEPTION_HANDLERS
from app.config.logging import setup_logging
from app.config.register_service import RegistryMicroservice
from app.config.kafka_config import start_kafka_consumer_tasks
from app.config.mongo_config import connect_to_mongo, close_mongo_connection
from app.notification.presentation.notification_controller import router as notification_router

from app.shared.middleware.logging_middleware import LoggingMiddleware
from app.shared.middleware.jwt_security import JwtAuthMiddleware


logger = logging.getLogger("app")

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up notification Service...")

    app.state.registry_client: Optional[RegistryMicroservice] = None

    if settings.REGISTRY_ENABLED:
        registry_client = RegistryMicroservice()
        registered, instance_id = await registry_client.perform_registry()
        if registered:
            logger.info(
                "Notification service registered with instance ID: %s",
                instance_id,
            )
            await registry_client.start_heartbeat_loop()
            app.state.registry_client = registry_client
        else:
            logger.error("Registry registration failed.")

    if settings.KAFKA_ENABLED:
        logger.info(
            "Kafka publishing enabled (bootstrap=%s, client_id=%s)",
            settings.KAFKA_BOOTSTRAP_SERVERS,
            settings.KAFKA_CLIENT_ID,
        )
    if settings.KAFKA_CONSUMER_ENABLED:
        logger.info(
            "Kafka consumer enabled (incoming_topic=%s)",
            settings.KAFKA_TOPIC_NOTIFICATION_INCOMING,
        )

    await connect_to_mongo()

    app.state.kafka_consumer_stop: Optional[asyncio.Event] = None
    app.state.kafka_consumer_tasks: List[asyncio.Task[None]] = []
    if settings.KAFKA_CONSUMER_ENABLED:
        stop_ev = asyncio.Event()
        app.state.kafka_consumer_stop = stop_ev
        app.state.kafka_consumer_tasks = start_kafka_consumer_tasks(stop_ev)

    yield

    logger.info("Shutting down notification Service...")
    tasks = getattr(app.state, "kafka_consumer_tasks", []) or []
    stop_ev = getattr(app.state, "kafka_consumer_stop", None)
    if stop_ev is not None:
        stop_ev.set()
    for t in tasks:
        t.cancel()
    for t in tasks:
        try:
            await t
        except asyncio.CancelledError:
            pass
    rc = getattr(app.state, "registry_client", None)
    if rc is not None and settings.REGISTRY_ENABLED:
        rc.stop_heartbeat_loop()
        await rc.aclose()

    await close_mongo_connection()


app = FastAPI(
    title="notification Service API",
    description=(
        "Cinema notification APIs: search and retrieve notifications, purchase flow, and "
        "showtime/seat reads backed by replicated billboard data (Mongo)."
    ),
    version=settings.API_VERSION,
    exception_handlers=GLOBAL_EXCEPTION_HANDLERS,
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_middleware(LoggingMiddleware)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(JwtAuthMiddleware)
app.include_router(notification_router)


@app.get("/health")
async def read_health():
    return {"status": "healthy", "service": "notification-service"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG_MODE,
        log_config=None,
    )
