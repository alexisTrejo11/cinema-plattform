# admin-service/main.py
from fastapi import FastAPI, HTTPException, status
import uvicorn
import datetime
import asyncio
from contextlib import asynccontextmanager
import aiohttp


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


async def perform_health_check(service_data: dict, instance_id: str):
    """Realiza una llamada de salud a un servicio."""
    url = f"http://{service_data['host']}:{service_data['port']}{service_data['health_check_endpoint']}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
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


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)
