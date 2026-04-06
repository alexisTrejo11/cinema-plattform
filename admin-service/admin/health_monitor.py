from .admin_service import RegistryService, ServiceStatus
import asyncio
import aiohttp
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class HealthMonitor:
    def __init__(
        self,
        service_registry: "RegistryService",
        check_interval: int = 10,
        timeout: int = 5,
    ):
        self.service_registry = service_registry
        self.check_interval = check_interval
        self.timeout = timeout
        self._running = False

    async def perform_health_check(self, instance_id: str) -> bool:
        """Performs a health check on a specific instance."""
        instance = self.service_registry.get_instance(instance_id)
        if not instance:
            logger.warning(f"Instance {instance_id} not found in registry")
            return False

        url = f"http://{instance.host}:{instance.port}{instance.health_check_endpoint}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url, timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    new_status = (
                        ServiceStatus.UP
                        if response.status == 200
                        else ServiceStatus.DOWN
                    )
                    self._update_instance_status(instance_id, new_status)
                    logger.info(
                        f"Health check for {instance_id}: {response.status} -> {new_status}"
                    )
                    return new_status == ServiceStatus.UP

        except Exception as e:
            self.service_registry.update_instance_status(
                instance_id, ServiceStatus.DOWN
            )
            logger.error(f"Health check for {instance_id} failed: {e} -> DOWN")
            return False

    def _update_instance_status(self, instance_id: str, status: ServiceStatus):
        """Safely updates the status of an instance."""
        instance = self.service_registry.get_instance(instance_id)
        if instance:
            instance.status = status
            instance.last_heartbeat = datetime.now()

    async def start_monitoring(self):
        """Starts continuous background monitoring."""
        self._running = True
        while self._running:
            try:
                await self.check_all_instances()
                await asyncio.sleep(self.check_interval)
            except asyncio.CancelledError:
                logger.info("Health monitoring stopped")
                break
            except Exception as e:
                logger.error(f"Error in health monitoring: {e}")
                await asyncio.sleep(self.check_interval)

    async def stop_monitoring(self):
        """Stops the monitoring."""
        self._running = False

    async def check_all_instances(self):
        """Performs health checks on all registered instances."""
        for instance_id in self.service_registry.get_all_instance_ids():
            await self.perform_health_check(instance_id)
