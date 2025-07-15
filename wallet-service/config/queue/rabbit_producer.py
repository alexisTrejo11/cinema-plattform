import json
from typing import Dict, Any
from rabbitmq_client import RabbitMQClient
import logging

logger = logging.getLogger("app")


class RabbitMQProducer(RabbitMQClient):
    def __init__(self, rabbitmq_url: str, exchange_name: str):
        super().__init__(rabbitmq_url, exchange_name)

    async def publish_message(self, message: Dict[str, Any], routing_key: str = ""):
        if not self.channel or not self.exchange:
            await self.connect()

        try:
            body = json.dumps(message).encode('utf-8')
            await self.exchange.publish(
                message=message.to_publish(body),
                routing_key=routing_key,
            )
            logger.info(f"Published message to exchange '{self.exchange_name}' with routing key '{routing_key}': {message}")
        except Exception as e:
            logger.warning(f"Error publishing message: {e}")
            raise