from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from pydantic import BaseModel
from .admin import registered_services, ServiceRegistration

app = APIRouter(prefix="/api/v2/admin-manager")


@app.post("/register-service", status_code=status.HTTP_201_CREATED)
async def register_service(registration: ServiceRegistration):
    """
    Endpoint para que los microservicios se registren.
    Genera un ID de instancia único si no se proporciona.
    """
    instance_id = f"{registration.service_name}-{registration.host}-{registration.port}"

    if registration.service_name not in registered_services:
        registered_services[registration.service_name] = {}

    registered_services[registration.service_name][instance_id] = {
        "host": registration.host,
        "port": registration.port,
        "health_check_endpoint": registration.health_check_endpoint,
        "last_heartbeat": datetime.now(),
        "status": "UNKNOWN",  # Estado inicial
    }
    print(f"Service '{registration.service_name}' registrado: {instance_id}")
    return {"message": "Service registered successfully", "instance_id": instance_id}


@app.post("/heartbeat/{service_name}/{instance_id}")
async def receive_heartbeat(service_name: str, instance_id: str):
    """
    Endpoint para que los servicios envíen un heartbeat.
    Actualiza el timestamp del último heartbeat.
    """
    if (
        service_name in registered_services
        and instance_id in registered_services[service_name]
    ):
        registered_services[service_name][instance_id][
            "last_heartbeat"
        ] = datetime.now()
        print(f"Heartbeat recibido de {service_name} ({instance_id})")
        return {"message": "Heartbeat received"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Service instance not found"
    )


@app.get("/available-services")
async def get_available_services():
    """
    Endpoint para obtener una lista de todos los servicios registrados y su estado.
    """
    response_data = []
    for service_name, instances in registered_services.items():
        for instance_id, data in instances.items():
            response_data.append(
                {
                    "service_name": service_name,
                    "instance_id": instance_id,
                    "host": data["host"],
                    "port": data["port"],
                    "status": data["status"],
                    "last_heartbeat": data["last_heartbeat"].isoformat(),
                }
            )
    return {"services": response_data}


@app.get("/available-services/{service_name}")
async def get_service_instances(service_name: str):
    """
    Endpoint para obtener instancias de un servicio específico.
    """
    if service_name in registered_services:
        instances_list = []
        for instance_id, data in registered_services[service_name].items():
            if data["status"] == "UP":
                instances_list.append(
                    {
                        "instance_id": instance_id,
                        "host": data["host"],
                        "port": data["port"],
                    }
                )
        if not instances_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No UP instances found for service {service_name}",
            )
        return {"service_name": service_name, "instances": instances_list}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Service '{service_name}' not found",
    )
