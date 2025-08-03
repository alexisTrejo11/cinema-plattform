from typing import Optional
import logging

from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from config.redis import RedisManager, get_redis
from config.model_init import *
from config.logging import setup_logging
from config import exception_handlers
from config.registry_service import RegistryMicroservice

from app.combos.infrastructure.api import combo_controllers
from app.products.infrastructure.api.controller import (
    category_controller,
    product_controller,
)
from app.promotions.infrastructure.api.controller import (
    promotion_command_controller,
    promotion_query_controllers,
    promotion_items_controller,
)
from app.shared.redis.redis_service import RedisService


setup_logging()
logger = logging.getLogger("app")
limiter = Limiter(key_func=get_remote_address, default_limits=["30/minute"])
registry_client: Optional[RegistryMicroservice] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting service...")

    # Registry Microservice
    registry_client = RegistryMicroservice()
    registered, instance_id = await registry_client.perfom_registry()

    await RedisManager.initialize()
    client = await get_redis()
    await RedisService.initialize(client)

    if registered:
        logger.info(
            f"Wallet Service successfully registered with instance ID: {instance_id}"
        )
        await registry_client.start_heartbeat_loop()
    else:
        logger.error("Failed to register Wallet Service. Heartbeats will not be sent.")

    yield

    # Shutdown process
    logger.info("Shutting down Wallet Service...")
    if registry_client:
        registry_client.stop_heartbeat_loop()
        logger.info("Heartbeat loop stopped.")

    await RedisManager.close()


app = FastAPI(
    lifespan=lifespan,
    title="Cinema Backend: Product Service API",
    debug=True,
    summary="Product Service for Cinema API that includes all product catalog and combos offers and all related to Product directly",
    version="1.0.0",
    exception_handlers=exception_handlers,
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "X-Requested-With",
        "Access-Control-Allow-Headers",
    ],
    expose_headers=["Content-Disposition"],
    max_age=600,
)


@app.get("/health", summary="Health Check")
def perform_health():
    return {"status": "ok", "message": "Product Service API is running"}


app.include_router(category_controller.router)
app.include_router(product_controller.router)
app.include_router(combo_controllers.router)
app.include_router(promotion_command_controller.router)
app.include_router(promotion_query_controllers.router)
app.include_router(promotion_items_controller.router)
