from fastapi import FastAPI
from app.products.infrastructure.api.controller import (
    category_controller,
    product_controller,
)
from app.combos.infrastructure.api import combo_controllers
from config.model_init import *
from config import exception_handlers
from config.logging import setup_logging
from contextlib import asynccontextmanager
import logging
from config.registry_service import RegistryMicroservice
from fastapi.middleware.cors import CORSMiddleware


setup_logging()
logger = logging.getLogger("app")


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

    yield

    # Shutdown process
    logger.info("Shutting down Wallet Service...")
    if registry_client:
        registry_client.stop_heartbeat_loop()
        logger.info("Heartbeat loop stopped.")


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
