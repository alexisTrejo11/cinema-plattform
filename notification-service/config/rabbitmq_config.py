import aio_pika
import asyncio
import logging
import os

logger = logging.getLogger("app")


class RabbitMQConnectionManager:
    """
    Gestiona la conexión robusta a RabbitMQ y proporciona canales.
    """

    def __init__(self):
        self.host = os.getenv("RQP_HOST", "rabbitmq_host")
        self.port = int(os.getenv("RQP_PORT", 5672))
        self.user = os.getenv("RQP_USER", "user")
        self.password = os.getenv("RQP_PASS", "password")
        self._connection = None
        self._channel = None
        self._connection_lock = asyncio.Lock()

    async def _connect(self):
        """Intenta establecer una conexión robusta a RabbitMQ."""
        if self._connection and not self._connection.is_closed:
            return self._connection

        async with self._connection_lock:
            if self._connection and not self._connection.is_closed:
                return self._connection

            try:
                logger.info(
                    f"Connecting to RabbitMQ at amqp://{self.user}:******@{self.host}:{self.port}"
                )
                self._connection = await aio_pika.connect_robust(
                    host=self.host,
                    port=self.port,
                    login=self.user,
                    password=self.password,
                )
                self._connection.add_close_callback(self._on_connection_close)  # type: ignore [attr-defined]
                logger.info("Successfully connected to RabbitMQ.")
                return self._connection
            except Exception as e:
                logger.error(f"Failed to connect to RabbitMQ: {e}")
                raise

    def _on_connection_close(self, sender, exc):
        """Callback cuando la conexión se cierra inesperadamente."""
        if exc:
            logger.error(
                f"RabbitMQ connection closed due to error: {exc}. Reconnecting..."
            )
        else:
            logger.info("RabbitMQ connection closed gracefully.")
        self._connection = None
        self._channel = None

    async def get_channel(self) -> aio_pika.abc.AbstractChannel:
        """Obtiene un canal de RabbitMQ, reconectando si es necesario."""
        if not self._channel or self._channel.is_closed:
            await self._connect()

            if not self._connection:
                logger.error("RabbitMQ connection is not established.")
                raise RuntimeError("RabbitMQ connection is not established.")

            self._channel = await self._connection.channel()
            logger.info("RabbitMQ channel obtained.")
        return self._channel

    async def close(self):
        """Cierra la conexión y el canal de RabbitMQ."""
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
            self._channel = None
            logger.info("RabbitMQ channel closed.")
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
            self._connection = None
            logger.info("RabbitMQ connection closed.")


async def get_rabbitmq_connection_manager() -> RabbitMQConnectionManager:
    manager = RabbitMQConnectionManager()
    try:
        await manager._connect()
    except Exception as e:
        logger.critical(f"Initial RabbitMQ connection failed: {e}. Exiting.")
        raise
    return manager
