from typing import Any, Dict

from fastapi import Depends, FastAPI, Request, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from config import exception_handlers as global_exception_handler
from config.app_config import Settings, get_settings
from config.model_init import *
from config.redis_config import get_redis_client

from app.users.infrastructure.controller import user_controllers
from app.auth.infrastructure.api import controllers as auth_controller
from app.profile.infrastructure import controllers as profile_controllers
from app.shared.logging import setup_logging 

setup_logging()
limiter = Limiter(key_func=get_remote_address, default_limits=["30/minute"])

app = FastAPI(
    title="Cinema Backend: User Service API",
    version="1.0.0",
    exception_handlers=global_exception_handler,
    )

# Rate Limiter
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Infor Endpoints
@app.get("/health")
def health_check():
    try:
        redis_client = get_redis_client()
        redis_client.ping()
        return {"status": "healthy", "redis": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {e}")

@app.get("/info")
async def get_app_info(settings: Settings = Depends(get_settings)) -> Dict[str, Any]:
    return {
        "app_name": "Cinema Backend: User Service API",
        "api_version": settings.API_VERSION,
        "debug_mode": settings.DEBUG_MODE,
        "database_url_prefix": settings.DATABASE_URL.split(":")[0]
    }

@app.get("/home/")
def read_home(request: Request) -> Any: 
    return {"home" : "Welcome to User Service" }

# Routing
app.include_router(user_controllers.router)
app.include_router(auth_controller.router)
app.include_router(profile_controllers.router)
