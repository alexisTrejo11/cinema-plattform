import pika
import json
import asyncio
from typing import Dict, Any
from aio_pika import connect_robust, RobustConnection, RobustChannel, ExchangeType, Message
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel
from config.app_config import get_settings
import logging

settings = get_settings()
logger = logging.getLogger("app")

class RabbitMQPublisher:
    def __init__(self):
        self.connection: AbstractRobustConnection  = None
        self.channel: AbstractRobustChannel  = None

    async def connect(self):
        """Establishes a robust connection to RabbitMQ and declares exchanges/queues."""
        try:
            self.connection = await connect_robust(settings.rabbitmq_url)
            self.channel = await self.connection.channel()

            # Declare exchanges
            await self.channel.declare_exchange(
                'notifications',
                ExchangeType.TOPIC,
                durable=True
            )

            # Declare queues and bind them
            # For 2FA notifications
            queue_2fa = await self.channel.declare_queue('2fa_notifications', durable=True)
            exchange = await self.channel.get_exchange('notifications')
            await queue_2fa.bind(
                exchange=exchange,
                routing_key='2fa.*' # Using a wildcard to catch all 2FA types
            )

            # For Account Activation notifications
            queue_activation = await self.channel.declare_queue('activation_acc_notifications', durable=True)
            await queue_activation.bind(
                exchange=exchange,
                routing_key='activation_acc.*' # Using a wildcard
            )
            logger.info("Successfully connected to RabbitMQ and declared exchanges/queues.")

        except Exception as e:
            logger.error(f"Error connecting to RabbitMQ: {e}", exc_info=True)
            # Re-raise to prevent the application from starting with a broken connection
            raise

    async def publish_2fa_request(self, user_email: str, token: str, notification_type: str = "email"):
        """Publishes a 2FA request message to RabbitMQ."""
        if not self.channel:
            logger.error("RabbitMQ channel is not established. Cannot publish message.")
            raise ConnectionError("RabbitMQ channel not available.")

        message_body = {
            "type": "2fa_request",
            "user_email": user_email,
            "token": token,
            "notification_type": notification_type,
            "timestamp": asyncio.get_event_loop().time()
        }

        try:
            message = Message(
                body=json.dumps(message_body).encode('utf-8'),
                content_type='application/json',
                delivery_mode=2 # Make message persistent
            )
            routing_key = f'2fa.{notification_type}'
            exchange = await self.channel.get_exchange('notifications')
            await exchange.publish(
                message,
                routing_key=routing_key
            )
            logger.info(f"2FA request sent for user: {user_email} with routing key: {routing_key}")
        except Exception as e:
            logger.error(f"Error publishing 2FA request for {user_email}: {e}", exc_info=True)
            raise

    async def close(self):
        """Closes the RabbitMQ connection."""
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            logger.info("RabbitMQ connection closed.")


# Singleton 
rabbitmq_publisher = RabbitMQPublisher()