from fastapi import FastAPI
import uvicorn
from config.app_config import settings
from config.mongo_config import connect_to_mongo, close_mongo_connection
from contextlib import asynccontextmanager 
from app.billboard_data.infrastructure import test_controller

app = FastAPI(
    debug=settings.app_debug, 
    version=settings.app_version,
    title=settings.app_name,
    summary=settings.app_summary
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await connect_to_mongo()
        yield
    except Exception as e:
        print(f"Error durante el startup: {e}")
        raise
    finally:
        await close_mongo_connection()


@app.get("/health")
def health_check():
        return {
            "status": "healthy", 
            "service": settings.app_name, 
            }

app.include_router(test_controller.router)

try:
    port = int(settings.app_port) if settings.app_port else 8000 
except (ValueError, TypeError):
    port = 8000
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)