from fastapi import FastAPI
from config.app_config import settings
import logging
from config.log_config import setup_logging
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware


app = FastAPI(
    title=settings.app_name,
    description=settings.app_summary,
    version=settings.app_version,
    debug=settings.app_debug,
)

# Logger
setup_logging()
logger = logging.getLogger("app")
audit_logger = logging.getLogger("audit")

# Rate Limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["30/minute"])
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


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
