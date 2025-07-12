from pydantic import BaseModel

registered_services = {}


class ServiceRegistration(BaseModel):
    service_name: str
    host: str
    port: int
    health_check_endpoint: str = "/health"
