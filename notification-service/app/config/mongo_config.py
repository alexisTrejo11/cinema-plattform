from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config.app_config import settings
import logging

logger = logging.getLogger(__name__)


class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None


mongo_db_client = MongoDB()


async def connect_to_mongo():
    """Create the MongoDB connection. Validates the connection on startup."""
    try:
        if mongo_db_client.client:
            mongo_db_client.client.close()

        mongo_db_client.client = AsyncIOMotorClient(
            settings.MONGO_URI,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=5000,
            socketTimeoutMS=5000,
        )

        await mongo_db_client.client.admin.command("ping")

        mongo_db_client.database = mongo_db_client.client[settings.MONGO_DB_NAME]

        logger.info("Connected to MongoDB: %s", settings.MONGO_DB_NAME)
        print(f"Connected to MongoDB: {settings.MONGO_DB_NAME}")

    except Exception as e:
        logger.error("Error connecting to MongoDB: %s", e)
        print(f"Error connecting to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close the MongoDB connection."""
    try:
        if mongo_db_client.client:
            mongo_db_client.client.close()
            mongo_db_client.client = None
            mongo_db_client.database = None
            logger.info("MongoDB connection closed")
            print("MongoDB connection closed")
    except Exception as e:
        logger.error("Error closing MongoDB connection: %s", e)


async def get_mongo_database() -> AsyncIOMotorDatabase:
    """Return the MongoDB database instance."""
    if mongo_db_client.database is None:
        logger.warning("No MongoDB connection; attempting to reconnect...")
        await connect_to_mongo()

        if mongo_db_client.database is None:
            raise RuntimeError("Could not establish MongoDB connection")

    return mongo_db_client.database


# FastAPI dependency helper
async def get_database_dependency() -> AsyncIOMotorDatabase:
    """Dependency that provides the database to endpoints."""
    return await get_mongo_database()
