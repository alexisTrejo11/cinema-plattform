# admin-service/main.py
from fastapi import FastAPI, HTTPException, status
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from contextlib import asynccontextmanager
import aiohttp
from admin.admin_service import RegistryService
from admin.health_monitor import HealthMonitor
from admin import admin_controller
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Admin Service started. Activating health monitor...")
    service_registry = RegistryService()
    health_monitor = HealthMonitor(service_registry)

    monitor_task = asyncio.create_task(health_monitor.start_monitoring())
    yield
    logger.info("Admin Service shutting down. Cancelling health monitor task.")

    await health_monitor.stop_monitoring()
    monitor_task.cancel()

    try:
        await monitor_task
    except asyncio.CancelledError:
        pass
        logger.info("Health monitor task cancelled successfully.")


app = FastAPI(
    title="Admin Service - Service Registry & Health Dashboard",
    description="Service for registering microservices and monitoring their health. Also for setting up queues and exchanges for RabbitMQ.",
    lifespan=lifespan,
)

origins = ["http://localhost:3000", "http://127.0.0.1", "http://127.0.0.1:8000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    with open("static/dashboard.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


app.include_router(admin_controller.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
