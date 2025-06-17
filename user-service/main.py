from typing import Any, Dict
from fastapi import Depends, FastAPI, Request, HTTPException
from config import exception_handlers as global_exception_handler
from config.app_config import Settings, get_settings
from config.model_init import *
from config.redis_config import get_redis_client
from app.users.infrastructure.controller import user_controllers
from app.auth.infrastructure.api import controllers as auth_controller

app = FastAPI(
    title="Cinema Backend: User Service API",
    version="1.0.0",
    exception_handlers=global_exception_handler,
    )

@app.get("/home/")
def home(request: Request): 
    return {"home" : "Welcome to User Service" }

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
        "api_version": settings.api_version,
        "debug_mode": settings.debug_mode,
        "database_url_prefix": settings.database_url.split(":")[0]
    }


app.include_router(user_controllers.router)
app.include_router(auth_controller.router)
