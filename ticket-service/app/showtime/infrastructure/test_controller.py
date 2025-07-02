from fastapi import APIRouter, HTTPException, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase 
from app.showtime.infrastructure.repository.mongo_theater_repo import MongoTheaterRepository
from config.mongo_config import get_mongo_database 

router = APIRouter(prefix="/test")

async def get_db_instance():
    """
    FastAPI dependency that provides the MongoDB database instance.
    This function internally calls get_mongo_database() which handles
    the actual connection lifecycle via the lifespan event.
    """

    return await get_mongo_database() 

async def get_theater_repo(db = Depends(get_db_instance)) -> MongoTheaterRepository:
    """
    FastAPI dependency that provides an instance of MongoTheaterRepository.
    """
    return MongoTheaterRepository(mongo_db=db)

@router.get("/theaters/")
async def get_theater_by_id(
    theater_repo: MongoTheaterRepository = Depends(get_theater_repo) 
):
    """
    Obtiene un teatro por su ID de negocio (int).
    """
    theaters = await theater_repo.get_all() 
        
    return  [theater.to_dict() for theater in theaters]


@router.get("/theaters/{theater_id}")
async def get_theater_by_id(
    theater_id: int,
    theater_repo: MongoTheaterRepository = Depends(get_theater_repo) 
):
    """
    Obtiene un teatro por su ID de negocio (int).
    """
    theater = await theater_repo.get_by_id(theater_id) 
    if not theater:
        raise HTTPException(status_code=404, detail="not found")
        
    return  theater.to_dict()

@router.get("/db-connection")
async def test_db_connection(db: AsyncIOMotorDatabase = Depends(get_db_instance)):
    """Probar conexión a la base de datos"""
    try:
        # Probar que podemos acceder a la base de datos
        collections = await db.list_collection_names()
        
        return {
            "status": "success",
            "message": "Conexión a MongoDB exitosa",
            "database_name": db.name,
            "collections_count": len(collections),
            "collections": collections[:5]  # Mostrar solo las primeras 5
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error conectando a la base de datos: {str(e)}"
        )