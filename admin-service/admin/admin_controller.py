from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from pydantic import BaseModel
from .admin_service import ServiceRegistration, RegistryService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v2/admin-manager")
service_registry = RegistryService()


@router.post("/register-service", status_code=status.HTTP_201_CREATED)
async def register_service(registration: ServiceRegistration):
    """
    Endpoint for microservices to register.
    Generates a unique instance ID if one is not provided.
    """
    instance_id = service_registry.register_service(registration)
    logger.info(
        f"Service '{registration.service_name}' registered with instance ID: {instance_id}"
    )
    return {"message": "Service registered successfully", "instance_id": instance_id}


@router.post("/heartbeat/{instance_id}")
async def receive_heartbeat(instance_id: str):
    """
    Endpoint for services to send a heartbeat.
    Updates the last heartbeat timestamp.
    """
    if not service_registry.update_heartbeat(instance_id):
        logger.warning(f"Heartbeat received for unknown instance ID: {instance_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service instance not found"
        )
    logger.debug(f"Heartbeat received for instance ID: {instance_id}")
    return {"message": "Heartbeat received"}


@router.get("/available-services")
async def get_available_services():
    """
    Endpoint to get a list of all registered services and their status.
    """
    services = service_registry.get_all_services()
    logger.debug("Retrieving all available services.")
    return {"services": services}


@router.get("/available-services/{service_name}")
async def get_service_instances(service_name: str):
    """
    Endpoint to get instances of a specific service.
    """
    instances = service_registry.get_service_instances(service_name)
    if not instances:
        logger.warning(f"No instances found for service: {service_name}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No instances found for service {service_name}",
        )
    logger.debug(f"Retrieving instances for service: {service_name}")
    return {"service_name": service_name, "instances": instances}
