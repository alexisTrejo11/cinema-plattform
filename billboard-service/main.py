import asyncio
import logging
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware
from fastapi.middleware.cors import CORSMiddleware

from app.config.app_config import settings
from app.config.rate_limit import limiter
from app.config.global_exception_handler import GLOBAL_EXCEPTION_HANDLERS
from app.config.logging import setup_logging
from app.config.postgres_config import engine, run_postgres_startup_check
from app.config.cache_config import close_cache, init_cache
from app.config.register_service import RegistryMicroservice
from app.config.kafka_config import shutdown_kafka, start_kafka_consumer_tasks

from app.shared.middleware.logging_middleware import LoggingMiddleware
from app.shared.middleware.jwt_security import JwtAuthMiddleware

from app.showtime.infrastructure.api import showtime_controller


logger = logging.getLogger(__name__)

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Billboard Service...")
    await run_postgres_startup_check(engine)
    await init_cache()

    app.state.registry_client: Optional[RegistryMicroservice] = None

    if settings.REGISTRY_ENABLED:
        registry_client = RegistryMicroservice()
        registered, instance_id = await registry_client.perfom_registry()
        if registered:
            logger.info(
                "Billboard Service registered with instance ID: %s",
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
            "Kafka consumer enabled (incoming_topic=%s, group=%s)",
            settings.KAFKA_TOPIC_Billboard_INCOMING,
            settings.KAFKA_CONSUMER_GROUP_Billboard,
        )

    app.state.kafka_consumer_stop: Optional[asyncio.Event] = None
    app.state.kafka_consumer_tasks: List[asyncio.Task[None]] = []
    if settings.KAFKA_CONSUMER_ENABLED:
        stop_ev = asyncio.Event()
        app.state.kafka_consumer_stop = stop_ev
        app.state.kafka_consumer_tasks = start_kafka_consumer_tasks(stop_ev)

    yield

    logger.info("Shutting down Billboard Service...")
    await close_cache()
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
    shutdown_kafka()
    rc = getattr(app.state, "registry_client", None)
    if rc is not None and settings.REGISTRY_ENABLED:
        rc.stop_heartbeat_loop()
        await rc.aclose()


app = FastAPI(
    title="Billboard Service API",
    description=(
        "Cinema Billboard APIs: Billboard methods, purchase intents, Billboard "
        "operations, and integration events for external services."
    ),
    version=settings.API_VERSION,
    exception_handlers=GLOBAL_EXCEPTION_HANDLERS,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.state.limiter = limiter

# Middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(JwtAuthMiddleware)

# API routers
app.include_router(showtime_controller.router)


@app.get("/health")
async def read_health():
    """ "
    Check the health of the service.
    Required from admin service to register the service and make health checks.
    """
    return {"status": "healthy", "service": "Billboard-service"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG_MODE,
        log_config=None,
    )
