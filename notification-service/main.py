
from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
def ping():
    """A simple ping endpoint to check if the service is alive."""
    return {"ping": "pong!"}

@app.get("/health")
def health_check():
    """A health check endpoint to verify the service is running correctly."""
    return {"status": "ok"}

