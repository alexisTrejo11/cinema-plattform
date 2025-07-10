from config.rabbitmq_config import RabbitMQConnectionManager
import aio_pika
import asyncio
import json
import logging

logger = logging.getLogger("app")


class RabbitMQConsumer:
    def __init__(self, rabbit_conn: RabbitMQConnectionManager) -> None:
        self.rabbit_conn = rabbit_conn
        self._channel = None
        self._consumer_tags = []

    async def start_consuming(self):
        try:
            self._channel = await self.rabbit_conn.get_channel()

            main_events_exchange = await self._channel.declare_exchange(
                name="main_events_exhange",
                type=aio_pika.ExchangeType.TOPIC,
                durable=True,
            )
            logger.info(
                f"Declared RabbitMQ consumer exchange: {main_events_exchange.name}"
            )

            # Notifications
            notifications_queue = await self._channel.declare_queue(
                name="incoming_notifications_queue", durable=True
            )
            await notifications_queue.bind(
                exchange=main_events_exchange,
                routing_key="notifications.#",
            )
            logger.info(
                f"Queue '{notifications_queue.name}' bound to '{main_events_exchange.name}' with routing key 'notifications.#'"
            )

            # Users
            user_changes_queue = await self._channel.declare_queue(
                name="user_changes_queue", durable=True
            )
            await user_changes_queue.bind(
                exchange=main_events_exchange, routing_key="user.changes.#"
            )
            logger.info(
                f"Queue '{user_changes_queue.name}' bound to '{main_events_exchange.name}' with routing key 'user.changes.#'"
            )

            logger.info("Starting RabbitMQ consumers...")
            self._consumer_tags.append(
                await notifications_queue.consume(self._on_notification_message)
            )
            self._consumer_tags.append(
                await user_changes_queue.consume(self._on_user_change_message)
            )

        except Exception as e:
            logger.error(f"Error starting RabbitMQ consumer: {e}", exc_info=True)
            raise

    async def _on_notification_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            try:
                payload = json.loads(message.body.decode())
                logger.info(
                    f"Received notification message (routing key: '{message.routing_key}'): {payload}"
                )

                # Add Impl

            except json.JSONDecodeError:
                logger.error(
                    f"Invalid JSON in notification message: {message.body.decode()}"
                )
                await message.reject(requeue=False)
            except Exception as e:
                logger.error(
                    f"Error processing user change message: {e}", exc_info=True
                )
                await message.reject(requeue=True)

    async def close(self):
        """Detiene el consumo y cierra la conexión."""
        for tag in self._consumer_tags:
            await self._channel.basic_cancel(tag)
            logger.info(f"Cancelled consumer tag: {tag}")
        self._consumer_tags = []
