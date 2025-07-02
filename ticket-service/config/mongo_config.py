from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config.app_config import settings
import logging

logger = logging.getLogger(__name__)

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None

mongo_db_client = MongoDB()

async def connect_to_mongo():
    """Crear conexión a MongoDB"""
    try:
        if mongo_db_client.client:
            mongo_db_client.client.close()
        
        mongo_db_client.client = AsyncIOMotorClient(
            settings.atlas_uri,
            serverSelectionTimeoutMS=5000,  # Timeout de 5 segundos
            connectTimeoutMS=5000,
            socketTimeoutMS=5000
        )
        
        await mongo_db_client.client.admin.command('ping')
        
        mongo_db_client.database = mongo_db_client.client[settings.mongo_db_name]
        
        logger.info(f"✅ Conectado exitosamente a MongoDB: {settings.mongo_db_name}")
        print(f"✅ Conectado exitosamente a MongoDB: {settings.mongo_db_name}")
        
    except Exception as e:
        logger.error(f"❌ Error conectando a MongoDB: {e}")
        print(f"❌ Error conectando a MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Cerrar conexión a MongoDB"""
    try:
        if mongo_db_client.client:
            mongo_db_client.client.close()
            mongo_db_client.client = None
            mongo_db_client.database = None
            logger.info("🔌 Conexión a MongoDB cerrada")
            print("🔌 Conexión a MongoDB cerrada")
    except Exception as e:
        logger.error(f"Error cerrando conexión MongoDB: {e}")

async def get_mongo_database() -> AsyncIOMotorDatabase:
    """Obtener instancia de la base de datos MongoDB"""
    if mongo_db_client.database is None:
        # Intentar reconectar si no hay conexión
        logger.warning("⚠️ No hay conexión a MongoDB, intentando reconectar...")
        await connect_to_mongo()
        
        if mongo_db_client.database is None:
            raise RuntimeError("No se pudo establecer conexión a MongoDB")
    
    return mongo_db_client.database

# Función de dependencia para FastAPI
async def get_database_dependency() -> AsyncIOMotorDatabase:
    """Dependencia para obtener la base de datos en los endpoints"""
    return await get_mongo_database()

