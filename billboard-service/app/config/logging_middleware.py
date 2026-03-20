import logging
from fastapi import Request, Response
from time import time
from uuid import uuid4

logger = logging.getLogger("app")
audit_logger = logging.getLogger("audit")

from typing import Callable, Awaitable

async def logging_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]):
    start_time = time()
    request_id = str(uuid4())
    
    audit_logger.info("Request received", extra={
        "props": {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "client": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
        }
    })

    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Request failed: {str(e)}", exc_info=True, extra={
            "props": {
                "request_id": request_id,
                "error": str(e),
            }
        })
        raise
    
    process_time = time() - start_time
    
    audit_logger.info("Request completed", extra={
        "props": {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "process_time": process_time,
        }
    })

    response.headers["X-Request-ID"] = request_id
    
    return response