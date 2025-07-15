import json
from aio_pika.abc import AbstractQueue, AbstractIncomingMessage
from typing import Optional, Dict, Any
from rabbitmq_client import RabbitMQClient
from app.user.infrastructure.queue.user_event_processor import UserEventProcessor
import logging

logger = logging.getLogger("app")


class RabbitMQConsumer(RabbitMQClient):
    def __init__(self, rabbitmq_url: str, exchange_name: str, queue_name: str):
        super().__init__(rabbitmq_url, exchange_name)
        self.queue_name = queue_name
        self.queue: Optional[AbstractQueue] = None
        self.event_processor = UserEventProcessor()

    async def connect(self):
        await super().connect()
        if self.channel:
            self.queue = await self.channel.declare_queue(self.queue_name, durable=True)
            await self.queue.bind(self.exchange)
            logger.info(f"Connected to RabbitMQ. Listening on queue '{self.queue_name}'...")

    async def start_consuming(self):
        await self.connect()
        if self.queue:
            await self.queue.consume(self.on_message)
            logger.info("Consumer started. Waiting for messages...")

    async def on_message(self, message: AbstractIncomingMessage):
        async with message.process():
            try:
                payload: Dict[str, Any] = json.loads(message.body.decode())
                await self.event_processor.process_user_event(payload)
            except json.JSONDecodeError:
                logger.error(f"Failed to decode JSON message: {message.body}")
                await message.reject(requeue=False)
            except Exception as e:
                logger.error(f"Error in on_message (dispatching to processor): {e}")
                await message.reject(requeue=False)

