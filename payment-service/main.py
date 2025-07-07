from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime

# Create FastAPI app instance
app = FastAPI(
    title="Payment Service API",
    description="A FastAPI microservice for managing cinema payments",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the service is running
    """
    return {
        "status": "healthy",
        "service": "payment-service",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

# Ping endpoint
@app.get("/ping", tags=["Health"])
async def ping():
    """
    Simple ping endpoint
    """
    return {
        "message": "pong",
        "timestamp": datetime.utcnow().isoformat()
    }

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with basic service information
    """
    return {
        "service": "Payment Service API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
