import asyncio
from aio_pika import connect_robust, ExchangeType
from aio_pika.abc import AbstractRobustConnection, AbstractChannel, AbstractExchange
from typing import Optional
import logging 

logger = logging.getLogger("app")

class RabbitMQClient:
    def __init__(self, rabbitmq_url: str, exchange_name: str):
        self.rabbitmq_url = rabbitmq_url
        self.exchange_name = exchange_name
        self.connection: Optional[AbstractRobustConnection] = None
        self.channel: Optional[AbstractChannel] = None
        self.exchange: Optional[AbstractExchange] = None
        
        
    async def connect(self):
        if self.connection and not self.connection.is_closed:
            logger.info("RabbitMQ connection already open.")
            return

        try:
            self.connection = await connect_robust(self.rabbitmq_url)
            self.channel = await self.connection.channel()
            self.exchange = await self.channel.declare_exchange(
                self.exchange_name,
                ExchangeType.TOPIC,
                durable=True,
            )
            logger.info(f"Connected to RabbitMQ at {self.rabbitmq_url}, exchange '{self.exchange_name}'.")
        except Exception as e:
            logger.error(f"Error connecting to RabbitMQ: {e}")
            raise
        
    async def close(self):
        if self.connection and not self.connection.is_closed:
            logger.info("Closing RabbitMQ connection...")
            
            await self.connection.close()
            self.connection = None
            self.channel = None
            self.exchange = None
            
            logger.info("RabbitMQ connection closed.")

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()