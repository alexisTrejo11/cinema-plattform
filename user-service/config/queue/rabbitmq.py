import aio_pika
import logging
from aio_pika import Connection, Channel
from config.app_config import settings

logger = logging.getLogger("app")

class RabbitMQPublisher:
    _connection: Connection | None = None
    _channel: Channel | None = None
    _is_connected: bool = False

    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url

    async def connect(self):
        """
        Attempts to establish a robust connection to RabbitMQ.
        If already connected and the connection is valid, it does nothing.
        Logs the connection status (success/failure).
        """
        if self._is_connected and self._connection and not self._connection.is_closed:
            logger.info("RabbitMQ: Connection is already established.")
            return

        logger.info(f"RabbitMQ: Attempting to connect to {self.amqp_url}...")
        try:
            self._connection = await aio_pika.connect_robust(self.amqp_url)
            self._channel = await self._connection.channel()
            self._is_connected = True
            logger.info("RabbitMQ: Connection established successfully!")
        except Exception as e:
            self._is_connected = False
            self._connection = None
            self._channel = None
            logger.error(f"RabbitMQ: Error connecting! Details: {e}", exc_info=True)
            raise ConnectionError(f"Could not connect to RabbitMQ: {e}")

    async def close(self):
        """
        Closes the RabbitMQ connection if it's open.
        """
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
            self._is_connected = False
            self._connection = None
            self._channel = None
            logger.info("RabbitMQ: Connection closed.")
        else:
            logger.info("RabbitMQ: No active connection to close.")

    def is_connected(self) -> bool:
        """
        Returns the current connection status.
        """
        return self._is_connected and self._connection and not self._connection.is_closed

    async def publish_token_request(self, user_email: str, token: str, notification_type: str):
        """
        Publishes a token request to RabbitMQ.
        Checks if the connection is active before publishing.
        """
        if not self.is_connected() or not self._channel:
            logger.error("RabbitMQ: Not connected. Failed to publish token request.")
            raise ConnectionError("RabbitMQ is not connected. Could not publish the message.")

        logger.info(f"RabbitMQ: Published message for {user_email} (type: {notification_type})")

rabbitmq_publisher = RabbitMQPublisher(amqp_url=settings.RABBITMQ_URL)