from fastapi import APIRouter, HTTPException, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase 
from config.mongo_config import get_mongo_database 
from app.external.billboard_data.infrastructure.repository.mongo_cinema_repo import MongoCinemaRepository

router = APIRouter(prefix="/test")

async def get_db_instance():
    """
    FastAPI dependency that provides the MongoDB database instance.
    This function internally calls get_mongo_database() which handles
    the actual connection lifecycle via the lifespan event.
    """

    return await get_mongo_database() 

async def get_cinema_repo(db = Depends(get_db_instance)) -> MongoCinemaRepository:
    """
    FastAPI dependency that provides an instance of MongocinemaRepository.
    """
    return MongoCinemaRepository(mongo_db=db)

@router.get("/cinemas/")
async def list_cinemas(
    cinema_repo: MongoCinemaRepository = Depends(get_cinema_repo) 
):
    """
    Obtiene un teatro por su ID de negocio (int).
    """
    cinemas = await cinema_repo.get_all() 
        
    return  [cinema.to_dict() for cinema in cinemas]


@router.get("/cinemas/{cinema_id}")
async def get_cinema_by_id(
    cinema_id: int,
    cinema_repo: MongoCinemaRepository = Depends(get_cinema_repo) 
):
    """
    Obtiene un teatro por su ID de negocio (int).
    """
    cinema = await cinema_repo.get_by_id(cinema_id) 
    if not cinema:
        raise HTTPException(status_code=404, detail="not found")
        
    return  cinema.to_dict()

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