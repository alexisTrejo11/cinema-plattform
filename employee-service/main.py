import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import (
    close_cache,
    global_exception_handler,
    init_cache,
    limiter,
    settings,
    setup_logging,
)
from app.employees.infrastructure.api.employee_controllers import router as employees_router
from app.schedules.infrastructure.api.schedule_controllers import router as schedules_router
from app.vacations.infrastructure.api.vacation_controllers import router as vacations_router

setup_logging()
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Cinema Platform - Employee Service",
        description="Microservice for managing cinema employees, schedules and vacation requests",
        version=settings.API_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    global_exception_handler.register(app)

    app.include_router(employees_router)
    app.include_router(schedules_router)
    app.include_router(vacations_router)

    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "ok", "service": "employee-service", "version": settings.API_VERSION}

    @app.on_event("startup")
    async def on_startup():
        await init_cache()
        logger.info("Employee service started")

    @app.on_event("shutdown")
    async def on_shutdown():
        await close_cache()
        logger.info("Employee service stopped")

    return app


app = create_app()
