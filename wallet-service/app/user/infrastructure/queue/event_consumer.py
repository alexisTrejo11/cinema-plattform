import asyncio
import json
from aio_pika import connect_robust, ExchangeType
from aio_pika.abc import (
    AbstractRobustConnection,
    AbstractChannel,
    AbstractQueue,
    AbstractExchange,
    AbstractIncomingMessage,
)
from typing import Dict, Any, Optional
from uuid import UUID
from app.user.domain.value_objects import UserId
from app.user.application.usecases import (
    CreateUserUseCase,
    UpdateUserUseCase,
    SoftDeleteUserUseCase,
)
from app.user.domain.repository import UserRepository
from app.user.infrastructure.sql_user_respository import (
    SqlAlchemyUserRepository,
)
from config.postgres_config import (
    AsyncSessionLocal,
    get_db as get_db_session,
)

RABBITMQ_URL = "amqp://guest:guest@localhost/"
USER_EVENTS_EXCHANGE = "user_events"


class RabbitMQConsumer:
    def __init__(self, rabbitmq_url: str, exchange_name: str, queue_name: str):
        self.rabbitmq_url = rabbitmq_url
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.connection: Optional[AbstractRobustConnection] = None
        self.channel: Optional[AbstractChannel] = None
        self.exchange: Optional[AbstractExchange] = None
        self.queue: Optional[AbstractQueue] = None

    async def connect(self):
        self.connection = await connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)

        self.exchange = await self.channel.declare_exchange(
            self.exchange_name,
            ExchangeType.FANOUT,
            durable=True,
        )

        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)
        await self.queue.bind(self.exchange)
        print(f"Connected to RabbitMQ. Listening on queue '{self.queue_name}'...")

    async def start_consuming(self):
        await self.connect()
        if self.queue:
            await self.queue.consume(self.on_message)
            print("Consumer started. Waiting for messages...")

    async def close(self):
        if self.connection:
            await self.connection.close()
            print("RabbitMQ connection closed.")

    async def on_message(self, message: AbstractIncomingMessage):
        async with message.process():
            try:
                payload: Dict[str, Any] = json.loads(message.body.decode())
                event_type = payload.get("type")
                user_data = payload.get("data")
                user_data = payload.get("data")

                if not event_type or not user_data:
                    print(f"Invalid message format: {payload}")
                    return

                # Get a new database session for each message processing
                async for session in get_db_session():
                    user_repo = SqlAlchemyUserRepository(session)

                    # Convert UUID strings in user_data to UUID objects if necessary
                    if "id" in user_data and isinstance(user_data["id"], str):
                        try:
                            user_data["id"] = UUID(user_data["id"])
                        except ValueError:
                            print(f"Invalid UUID format for user_id: {user_data['id']}")
                            return

                    if event_type == "user.created":
                        use_case = CreateUserUseCase(user_repo)
                        await use_case.execute(user_data)
                        print(f"User created: {user_data.get('email')}")
                    elif event_type == "user.updated":
                        user_id = str(
                            user_data.get("id")
                        )  # Ensure ID is string for use case
                        if user_id:
                            use_case = UpdateUserUseCase(user_repo)
                            await use_case.execute(
                                UserId.from_string(user_id), user_data
                            )
                            print(f"User updated: {user_id}")
                        else:
                            print(f"Update event missing user ID: {payload}")
                    elif event_type == "user.deleted":
                        user_id = str(
                            user_data.get("id")
                        )  # Ensure ID is string for use case
                        if user_id:
                            use_case = SoftDeleteUserUseCase(user_repo)
                            await use_case.execute(UserId.from_string(user_id))
                            print(f"User deleted: {user_id}")
                        else:
                            print(f"Delete event missing user ID: {payload}")
                    else:
                        print(f"Unknown event type: {event_type}")

            except json.JSONDecodeError:
                print(f"Failed to decode JSON message: {message.body}")
            except Exception as e:
                print(f"Error processing message: {e}")
                await message.reject(requeue=False)  #  rejecting without re-queuing
