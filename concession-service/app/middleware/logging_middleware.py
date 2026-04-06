import logging
from time import time
from typing import Awaitable, Callable
from uuid import uuid4

from fastapi import Request, Response

logger = logging.getLogger("app")
audit_logger = logging.getLogger("audit")


async def logging_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
):
    start_time = time()
    request_id = str(uuid4())

    audit_logger.info(
        "Request received",
        extra={
            "props": {
                "event": "http_request_start",
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "client": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent"),
            }
        },
    )

    try:
        response = await call_next(request)
    except Exception as e:
        process_time = time() - start_time
        audit_logger.error(
            "Request failed",
            extra={
                "props": {
                    "event": "http_request_error",
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "process_time": process_time,
                    "error": str(e),
                }
            },
            exc_info=True,
        )
        logger.error(
            f"{request.method} {request.url.path} failed {process_time:.3f}s "
            f"request_id={request_id} error={e!s}",
            exc_info=True,
            extra={
                "props": {
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(e),
                    "process_time": process_time,
                }
            },
        )
        raise

    process_time = time() - start_time

    audit_logger.info(
        "Request completed",
        extra={
            "props": {
                "event": "http_request_complete",
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time": process_time,
            }
        },
    )

    logger.info(
        f"{request.method} {request.url.path} {response.status_code} "
        f"{process_time:.3f}s request_id={request_id}",
        extra={
            "props": {
                "event": "http_request",
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(process_time * 1000, 3),
                "process_time": process_time,
            }
        },
    )

    response.headers["X-Request-ID"] = request_id

    return response
