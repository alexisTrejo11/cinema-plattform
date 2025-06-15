from fastapi import FastAPI, Request, HTTPException
from config import exception_handlers as global_exception_handler

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
async def health_check():
    try:
        redis_client = get_redis_client()
        redis_client.ping()
        return {"status": "healthy", "redis": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {e}")

app.include_router(user_controllers.router)
app.include_router(auth_controller.router)
