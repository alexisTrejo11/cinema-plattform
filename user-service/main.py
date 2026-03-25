from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.auth.infrastructure.api import auth_controllers, two_fa_controllers
from app.middleware.auth_middleware import jwt_auth_middleware
from app.profile.infrastructure import controllers as profile_controllers
from app.users.infrastructure.controller import user_controllers
from app.shared.logging import setup_logging
from app.config import exception_handlers
from app.config.app_config import settings
from app.config.cache_config import close_cache, init_cache
from app.config.database_startup import run_postgres_startup_check
from app.config.postgres_config import engine

setup_logging()
logger = logging.getLogger("app")
limiter = Limiter(key_func=get_remote_address, default_limits=["30/minute"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting User Service...")
    await run_postgres_startup_check(engine)
    await init_cache()
    logger.info("Redis cache ready.")
    yield
    logger.info("Shutting down User Service...")
    await close_cache()
    logger.info("User Service stopped.")


app = FastAPI(
    title="Cinema Backend: User Service API",
    version="1.0.0",
    lifespan=lifespan,
    exception_handlers=exception_handlers,
)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
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
app.middleware("http")(jwt_auth_middleware)


@app.get("/health", summary="Health Check")
def health_check() -> dict[str, str]:
    return {"status": "ok", "message": "User Service API is running"}


@app.get("/info")
async def get_app_info() -> dict[str, Any]:
    return {
        "app_name": "Cinema Backend: User Service API",
        "api_version": settings.API_VERSION,
        "debug_mode": str(settings.DEBUG_MODE),
        "database_url_prefix": settings.postgres_db_url().split(":")[0],
    }


@app.get("/home/")
def read_home(request: Request) -> Any:
    return {"home": "Welcome to User Service"}


app.include_router(user_controllers.router)
app.include_router(auth_controllers.router)
app.include_router(two_fa_controllers.router)
app.include_router(profile_controllers.router)
