from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config.app_config import settings
import logging

logger = logging.getLogger(__name__)


class MongoDB:
    """
    Manages the MongoDB client and database instances.
    """

    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.database: Optional[AsyncIOMotorDatabase] = None


mongo_db_client = MongoDB()


async def connect_to_mongo():
    """
    Establishes a connection to MongoDB.
    """
    try:
        if mongo_db_client.client:
            mongo_db_client.client.close()

        mongo_db_client.client = AsyncIOMotorClient(
            settings.atlas_uri,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=5000,
        )

        await mongo_db_client.client.admin.command("ping")

        mongo_db_client.database = mongo_db_client.client[settings.mongo_db_name]

        logger.info(f"✅ Successfully connected to MongoDB: {settings.mongo_db_name}")
        print(f"✅ Successfully connected to MongoDB: {settings.mongo_db_name}")

    except Exception as e:
        logger.error(f"❌ Error connecting to MongoDB: {e}")
        print(f"❌ Error connecting to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """
    Closes the MongoDB connection.
    """
    try:
        if mongo_db_client.client:
            mongo_db_client.client.close()
            mongo_db_client.client = None
            mongo_db_client.database = None
            logger.info("🔌 MongoDB connection closed")
            print("🔌 MongoDB connection closed")
    except Exception as e:
        logger.error(f"Error closing MongoDB connection: {e}")


async def get_mongo_database() -> AsyncIOMotorDatabase:
    """
    Retrieves the MongoDB database instance.
    """
    if mongo_db_client.database is None:
        logger.warning("⚠️ No MongoDB connection, attempting to reconnect...")
        await connect_to_mongo()

        if mongo_db_client.database is None:
            raise RuntimeError("Failed to establish MongoDB connection")

    return mongo_db_client.database


async def get_database_dependency() -> AsyncIOMotorDatabase:
    """
    Dependency to get the database instance for endpoints.
    """
    return await get_mongo_database()
