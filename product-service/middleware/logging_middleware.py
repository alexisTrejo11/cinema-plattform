import logging
from uuid import uuid4
from time import time
from typing import Callable, Awaitable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger("app")
audit_logger = logging.getLogger("audit")


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    A class-based middleware for logging incoming requests and outgoing responses,
    including request IDs for tracing.
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        Processes the request, logs details, and adds a request ID to the response headers.
        """
        start_time = time()
        request_id = str(uuid4())

        request.state.request_id = request_id

        audit_logger.info(
            "Request received",
            extra={
                "props": {
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "query_params": dict(request.query_params),
                    "client": request.client.host if request.client else None,
                    "user_agent": request.headers.get("user-agent"),
                }
            },
        )

        response = Response(
            "Internal Server Error", status_code=500
        )  # Default response in case of uncaught error
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(
                f"Request failed: {str(e)}",
                exc_info=True,
                extra={
                    "props": {
                        "request_id": request_id,
                        "error": str(e),
                    }
                },
            )
            raise
        finally:
            process_time = time() - start_time

            audit_logger.info(
                "Request completed",
                extra={
                    "props": {
                        "request_id": request_id,
                        "method": request.method,
                        "path": request.url.path,
                        "status_code": response.status_code,
                        "process_time": process_time,
                    }
                },
            )

            if hasattr(response, "headers"):
                response.headers["X-Request-ID"] = request_id

        return response
