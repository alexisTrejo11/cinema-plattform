import logging
from typing import Optional 
from pydantic import BaseModel
from config.app_config import settings
import aiohttp
import asyncio

logger = logging.getLogger("app")

class ServiceRegistration(BaseModel):
    service_name: str
    host: str
    port: int
    health_check_endpoint: str = "/health"
    instance_id: Optional[str] = None

class RegistryMicroservice:
    def __init__(self) -> None:
        self.timeout = 20
        self.service_data = ServiceRegistration(
            service_name="WALLET-SERVICE",
            host="localhost",
            port=8081,
            health_check_endpoint="/health"
        )
        self.registry_base_url = "http://localhost:8000/api/v2/admin-manager"
        self.heartbeat_interval_seconds = 30
        self._heartbeat_task: Optional[asyncio.Task] = None
        
        
    async def perfom_registry(self):
        registration_url = f"{self.registry_base_url}/register-service"
        payload = self.service_data.model_dump()

        logger.info(f"Attempting to register service at {registration_url} with data: {payload}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    registration_url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    if response.status == 201:
                        response_data = await response.json()
                        instance_id = response_data.get("instance_id")
                        
                        logger.info(f"Service registered successfully. Instance ID: {instance_id}")
                        self.service_data.instance_id = instance_id
                        
                        return True, instance_id
                    else:
                        error_message = await response.text()
                        logger.error(
                            f"Service registration failed with status {response.status}: {error_message}"
                        )
                        return False, None
        except aiohttp.ClientError as e:
            logger.error(f"Network or client error during service registration: {e}")
            return False, None
        except asyncio.TimeoutError:
            logger.error(f"Timeout occurred during service registration after {self.timeout} seconds.")
            return False, None
        except Exception as e:
            logger.error(f"An unexpected error occurred during service registration: {e}")
            return False, None
        
        
    async def perfom_heartbeat(self):
        if not self.service_data.instance_id:
            logger.warning("Cannot send heartbeat: instance_id is not set. Service might not be registered.")
            return False

        heartbeat_url = f"{self.registry_base_url}/heartbeat/{self.service_data.instance_id}"

        logger.debug(f"Sending heartbeat to {heartbeat_url}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    heartbeat_url,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    if response.status == 200:
                        logger.debug(f"Heartbeat successful for instance ID: {self.service_data.instance_id}")
                        return True
                    else:
                        error_message = await response.text()
                        logger.error(
                            f"Heartbeat failed for instance ID {self.service_data.instance_id} "
                            f"with status {response.status}: {error_message}"
                        )
                        return False
        except aiohttp.ClientError as e:
            logger.error(f"Network or client error during heartbeat for {self.service_data.instance_id}: {e}")
            return False
        except asyncio.TimeoutError:
            logger.error(f"Timeout occurred during heartbeat for {self.service_data.instance_id} after {self.timeout} seconds.")
            return False
        except Exception as e:
            logger.error(f"An unexpected error occurred during heartbeat for {self.service_data.instance_id}: {e}")
            return False

    async def start_heartbeat_loop(self):
        if self._heartbeat_task and not self._heartbeat_task.done():
            logger.info("Heartbeat loop is already running.")
            return

        async def _loop():
            while True:
                await self.perfom_heartbeat()
                await asyncio.sleep(self.heartbeat_interval_seconds)

        logger.info(f"Starting heartbeat loop, sending every {self.heartbeat_interval_seconds} seconds.")
        self._heartbeat_task = asyncio.create_task(_loop())

    def stop_heartbeat_loop(self):
        if self._heartbeat_task:
            logger.info("Stopping heartbeat loop.")
            self._heartbeat_task.cancel()
            self._heartbeat_task = None