from fastapi import FastAPI
from config.app_config import settings
import logging
from config.log_config import setup_logging

app = FastAPI(
    title=settings.app_name,
    description=settings.app_summary,
    version=settings.app_version,
    debug=settings.app_debug,
)

setup_logging()

logger = logging.getLogger("app")
audit_logger = logging.getLogger("audit")


@app.get("/ping")
def ping():
    """A simple ping endpoint to check if the service is alive."""
    logger.debug("Debug log from ping endpoint (will not show with INFO level)")
    logger.info("Ping endpoint called successfully!")
    return {"ping": "pong!"}


@app.get("/health")
def health_check():
    """A health check endpoint to verify the service is running correctly."""
    logger.info("Health check passed.")
    audit_logger.info("Audit: Health check event.")
    return {"status": "ok"}
