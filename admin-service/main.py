# admin-service/main.py
from fastapi import FastAPI, HTTPException, status
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from contextlib import asynccontextmanager
import aiohttp
from admin.admin import registered_services
from admin import admin_controller
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse


# Admin config
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Admin Service iniciado. Activando monitor de salud...")
    health_monitor_task = asyncio.create_task(health_check_monitor())
    yield
    print("Admin Service cerrando. Cancelando tarea de monitor de salud.")
    health_monitor_task.cancel()
    try:
        await health_monitor_task
    except asyncio.CancelledError:
        print("Tarea de monitor de salud cancelada exitosamente.")


app = FastAPI(
    title="Admin Service - Service Registry & Health Dashboard",
    description="Servicio para registrar microservicios y monitorear su salud.",
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


async def perform_health_check(service_data: dict, instance_id: str):
    """Realiza una llamada de salud a un servicio."""
    url = f"http://{service_data['host']}:{service_data['port']}{service_data['health_check_endpoint']}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                if response.status == 200:
                    registered_services[service_data["service_name"]][instance_id][
                        "status"
                    ] = "UP"
                else:
                    registered_services[service_data["service_name"]][instance_id][
                        "status"
                    ] = "DOWN"
                print(
                    f"Health check for {instance_id}: {response.status} -> {registered_services[service_data['service_name']][instance_id]['status']}"
                )
    except Exception as e:
        registered_services[service_data["service_name"]][instance_id][
            "status"
        ] = "DOWN"
        print(f"Health check for {instance_id} failed: {e} -> DOWN")


async def health_check_monitor():
    """Tarea en segundo plano para monitorear la salud de los servicios."""
    while True:
        if asyncio.current_task().done():
            break
        for service_name, instances in registered_services.items():
            for instance_id, data in instances.items():
                await perform_health_check(data, instance_id)
        await asyncio.sleep(10)


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    with open("static/dashboard.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


app.include_router(admin_controller.app)

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)
