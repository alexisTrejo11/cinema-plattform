from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.wallet.presentation.controllers import wallet_controller
from app.user.presentation import user_admin_controller
from config.app_config import settings
import asyncio
from config.global_exception_handler import GLOBAL_EXCEPTION_HANDLERS
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from config.logging import setup_logging 
from middleware.logging_middleware import LoggingMiddleware 

setup_logging()
limiter = Limiter(key_func=get_remote_address, default_limits=["30/minute"])

"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(
        "Application startup: Initializing database and starting RabbitMQ consumer..."
    )
    
    app.state.rabbitmq_consumer = RabbitMQConsumer(
        settings.RABBITMQ_URL,
        settings.USER_EVENTS_EXCHANGE,
        settings.CONSUMER_QUEUE_NAME,
    )
    app.state.consumer_task = asyncio.create_task(
        app.state.rabbitmq_consumer.start_consuming()
    )

    yield

    print("Application shutdown: Closing RabbitMQ consumer and database connections...")

    if app.state.consumer_task:
        app.state.consumer_task.cancel()
        try:
            await app.state.consumer_task
        except asyncio.CancelledError:
            print("RabbitMQ consumer task cancelled successfully.")
        except Exception as e:
            print(f"Error during consumer task cancellation: {e}")

    if app.state.rabbitmq_consumer:
        await app.state.rabbitmq_consumer.close()
        print("RabbitMQ connection closed.")
    """


app = FastAPI(
    title="Wallet Service API",
    description="API for managing wallets and users.",
    version="1.0.0",
    exception_handlers=GLOBAL_EXCEPTION_HANDLERS,
    #lifespan=lifespan,
)

app.state.limiter = limiter
app.add_middleware(LoggingMiddleware)
app.add_middleware(SlowAPIMiddleware)

@app.get("/")
async def read_root():
    return {"message": "Wallet Service is running and listening for user events!"}


app.include_router(wallet_controller.router)
app.include_router(user_admin_controller.router)
