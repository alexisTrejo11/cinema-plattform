from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware

from app.cinema.infrastructure.api import cinema_controllers  # noqa: E402
from app.config.app_config import settings  # noqa: E402
from app.config.global_exception_handler import GLOBAL_EXCEPTION_HANDLERS  # noqa: E402
from app.config.logging import setup_logging  # noqa: E402
from app.config.postgres_config import engine, run_postgres_startup_check  # noqa: E402
from app.config.rate_limit import limiter  # noqa: E402
from app.grpc.catalog_server import create_catalog_grpc_server  # noqa: E402
from app.movies.infrastructure.api import movie_controllers  # noqa: E402
from app.shared.middleware.jwt_security import JwtAuthMiddleware  # noqa: E402
from app.shared.middleware.logging_middleware import LoggingMiddleware  # noqa: E402
from app.theater.infrastructure.api import theather_seat_controllers, theater_controllers  # noqa: E402


logger = logging.getLogger(__name__)
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Catalog Service...")
    await run_postgres_startup_check(engine)

    grpc_server = create_catalog_grpc_server()
    await grpc_server.start()
    logger.info("Catalog gRPC listening on %s:%s", settings.GRPC_HOST, settings.GRPC_PORT)
    app.state.grpc_server = grpc_server
    app.state.grpc_wait_task = asyncio.create_task(grpc_server.wait_for_termination())

    yield

    logger.info("Shutting down Catalog Service...")
    wait_task: asyncio.Task[None] = app.state.grpc_wait_task
    grpc_server = app.state.grpc_server
    await grpc_server.stop(grace=5)
    wait_task.cancel()


app = FastAPI(
    title="Catalog Service API",
    description="Catalog APIs for cinemas, theaters, and movies.",
    version=settings.API_VERSION,
    exception_handlers=GLOBAL_EXCEPTION_HANDLERS,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.limiter = limiter
app.add_middleware(LoggingMiddleware)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(JwtAuthMiddleware)

app.include_router(cinema_controllers.router)
app.include_router(movie_controllers.router)
app.include_router(theater_controllers.router)
app.include_router(theather_seat_controllers.router)


@app.get("/health")
async def read_health():
    return {"status": "healthy", "service": "catalog-service"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG_MODE,
        log_config=None,
    )
