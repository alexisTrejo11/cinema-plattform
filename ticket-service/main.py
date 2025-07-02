from fastapi import FastAPI
import uvicorn
from config.app_config import settings

app = FastAPI(
    debug=settings.app_debug, 
    version=settings.app_version,
    title=settings.app_name,
    summary=settings.app_summary
    )


@app.get("/health")
def health_check():
        return {"status": "healthy", "service": settings.app_name, }

try:
    port = int(settings.app_port) if settings.app_port else 8000 
except (ValueError, TypeError):
    port = 8000
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)