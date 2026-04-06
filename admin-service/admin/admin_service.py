from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Dict, List, Optional, Set
from collections import defaultdict


class ServiceStatus(str, Enum):
    UNKNOWN = "UNKNOWN"
    UP = "UP"
    DOWN = "DOWN"


class ServiceInstance(BaseModel):
    host: str
    port: int
    health_check_endpoint: str
    last_heartbeat: datetime
    status: ServiceStatus = ServiceStatus.UNKNOWN
    service_name: Optional[str] = None


class ServiceRegistration(BaseModel):
    service_name: str
    host: str
    port: int
    health_check_endpoint: str = "/health"


class RegistryService:
    def __init__(self) -> None:
        self._instances: Dict[str, ServiceInstance] = {}  # ID -> Instance
        self._service_index: defaultdict[str, Set[str]] = defaultdict(set)  # NAME -> ID

    def register_service(self, registration: ServiceRegistration) -> str:
        instance_id = (
            f"{registration.service_name}-{registration.host}-{registration.port}"
        )

        instance = ServiceInstance(
            host=registration.host,
            port=registration.port,
            health_check_endpoint=registration.health_check_endpoint,
            last_heartbeat=datetime.now(),
            service_name=registration.service_name,
        )

        self._instances[instance_id] = instance
        self._service_index[registration.service_name].add(instance_id)
        return instance_id

    def get_instance(self, instance_id: str) -> Optional[ServiceInstance]:
        return self._instances.get(instance_id)

    def get_service_instances(self, service_name: str) -> List[ServiceInstance]:
        return [
            self._instances[instance_id]
            for instance_id in self._service_index.get(service_name, set())
        ]

    def get_all_services(self):
        services = []
        for name, ids in self._service_index.items():
            services.append([self._instances[instance_id] for instance_id in ids])
        return services

    def update_heartbeat(self, instance_id: str) -> bool:
        instance = self._instances.get(instance_id)
        if not instance:
            return False

        instance.last_heartbeat = datetime.now()
        return True

    def update_instance_status(
        self, instance_id: str, new_status: ServiceStatus
    ) -> bool:
        instance = self._instances.get(instance_id)
        if not instance:
            return False

        instance.status = new_status
        return True

    def get_all_instance_ids(self) -> List[str]:
        return list(self._instances.keys())
