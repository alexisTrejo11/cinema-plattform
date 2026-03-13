from contextlib import asynccontextmanager
import logging as py_logging

from fastapi import FastAPI, Request

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from model_initialization import *
from app.config import exception_handlers
from app.config.logging_config import setup_logging

from app.core.movies.infrastructure.api import movie_controllers
from app.core.movies.infrastructure.api import movie_showtime_controller
from app.core.cinema.infrastructure.api import cinema_controllers
from app.core.showtime.infrastructure.api import showtime_controller
from app.core.theater.infrastructure.api import (
    theater_controllers,
    theather_seat_controllers,
)
from app.config.postgres_config import verify_db_connection, engine
from app.config.jwt_auth_middleware import jwt_auth_middleware
from app.config.app_config import settings
from app.config.cache_config import init_cache, close_cache

setup_logging()
logger = py_logging.getLogger("app")
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Stop the server startup if PostgreSQL is unreachable.
    await verify_db_connection()
    await init_cache()
    try:

        yield
    finally:
        await engine.dispose()
        await close_cache()
        logger.info("Application shutdown complete")


fast_api_app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    exception_handlers=exception_handlers,
    lifespan=lifespan,
)

# Add the limiter to the FastAPI app state and include the SlowAPIMiddleware
fast_api_app.state.limiter = limiter
fast_api_app.add_middleware(SlowAPIMiddleware)
fast_api_app.middleware("http")(jwt_auth_middleware)


@fast_api_app.get("/")
@limiter.limit("5/minute")
def read_home(request: Request):
    return {"home": "Welcome To Billboard Service"}


fast_api_app.include_router(movie_controllers.router)
fast_api_app.include_router(movie_showtime_controller.router)

fast_api_app.include_router(cinema_controllers.router)

fast_api_app.include_router(theater_controllers.router)
fast_api_app.include_router(theather_seat_controllers.router)

fast_api_app.include_router(showtime_controller.router)
