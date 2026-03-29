import logging
import os
from time import time
from typing import Awaitable, Callable, Optional
from uuid import uuid4

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger("app")
audit_logger = logging.getLogger("audit")
audit_summary_logger = logging.getLogger("audit.http")

# always = IN + OUT console line every request; auto = both lines only for notable requests; never = file only
_AUDIT_CONSOLE_MODE = os.environ.get("AUDIT_CONSOLE", "always").strip().lower()
_AUDIT_SLOW_MS = float(os.environ.get("AUDIT_SLOW_MS", "2000"))
_SIMPLE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})
_UA_MAX = 96


def _short(text: Optional[str], max_len: int = _UA_MAX) -> Optional[str]:
    if not text:
        return None
    s = text.strip()
    if len(s) <= max_len:
        return s
    return s[: max_len - 3] + "..."


def _should_emit_audit_console_pair(
    request: Request,
    status_code: int,
    process_time_s: float,
    *,
    is_error: bool,
) -> bool:
    if _AUDIT_CONSOLE_MODE == "never":
        return False
    if _AUDIT_CONSOLE_MODE == "always":
        return True
    if is_error or status_code >= 400:
        return True
    if request.query_params:
        return True
    if request.method not in _SIMPLE_METHODS:
        return True
    if process_time_s * 1000.0 >= _AUDIT_SLOW_MS:
        return True
    return False


def _audit_start_props(request: Request, request_id: str) -> dict:
    return {
        "event": "http_audit",
        "phase": "start",
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "query_params": dict(request.query_params),
        "client": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        "content_type": request.headers.get("content-type"),
        "content_length": request.headers.get("content-length"),
        "accept": _short(request.headers.get("accept"), 64),
    }


def _build_audit_in_line(request: Request, request_id: str) -> str:
    parts = [
        "AUDIT IN ",
        request.method,
        " ",
        request.url.path,
        " id=",
        request_id,
    ]
    client = request.client.host if request.client else None
    if client:
        parts.extend([" client=", client])
    if request.query_params:
        parts.extend([" query=", repr(dict(request.query_params))])
    ct = request.headers.get("content-type")
    if ct:
        parts.extend([" ctype=", _short(ct, 48) or ct])
    cl = request.headers.get("content-length")
    if cl:
        parts.extend([" clen=", cl])
    ua = _short(request.headers.get("user-agent"))
    if ua:
        parts.extend([' ua="', ua, '"'])
    return "".join(parts)


def _build_audit_out_line(
    request: Request,
    request_id: str,
    status_code: int,
    process_time_s: float,
    *,
    response: Optional[Response] = None,
    error: Optional[str] = None,
) -> str:
    duration_ms = round(process_time_s * 1000.0, 2)
    parts = [
        "AUDIT OUT ",
        request.method,
        " ",
        request.url.path,
        " → ",
        str(status_code),
        " in ",
        str(duration_ms),
        "ms id=",
        request_id,
    ]
    if response is not None:
        rct = response.headers.get("content-type")
        if rct:
            parts.extend([" rctype=", _short(rct, 48) or rct])
        rcl = response.headers.get("content-length")
        if rcl:
            parts.extend([" rclen=", rcl])
    if error:
        parts.extend([" error=", _short(error, 120) or error])
    return "".join(parts)


def _emit_audit_console_pair(
    request: Request,
    request_id: str,
    *,
    status_code: int,
    process_time_s: float,
    response: Optional[Response] = None,
    error: Optional[str] = None,
    is_error: bool,
) -> None:
    if not _should_emit_audit_console_pair(
        request, status_code, process_time_s, is_error=is_error
    ):
        return
    if _AUDIT_CONSOLE_MODE == "auto":
        # Defer IN until we know the request is worth logging; emit IN then OUT together.
        audit_summary_logger.info(_build_audit_in_line(request, request_id))
    audit_summary_logger.info(
        _build_audit_out_line(
            request,
            request_id,
            status_code,
            process_time_s,
            response=response,
            error=error,
        )
    )


class LoggingMiddleware(BaseHTTPMiddleware):
    """HTTP audit: JSON start+complete in audit.log; console IN/OUT summaries."""

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time()
        request_id = str(uuid4())
        request.state.request_id = request_id

        audit_logger.info(
            "http_request_start",
            extra={"props": _audit_start_props(request, request_id)},
        )

        if _AUDIT_CONSOLE_MODE == "always":
            audit_summary_logger.info(_build_audit_in_line(request, request_id))

        try:
            response = await call_next(request)
        except Exception as e:
            process_time = time() - start_time
            err = str(e)
            audit_logger.error(
                "http_request_failed",
                extra={
                    "props": {
                        "event": "http_audit",
                        **_audit_start_props(request, request_id),
                        "phase": "failed",
                        "status_code": 500,
                        "duration_ms": round(process_time * 1000.0, 3),
                        "error": err,
                    }
                },
                exc_info=True,
            )
            logger.error(
                "Request failed",
                exc_info=True,
                extra={
                    "props": {
                        "request_id": request_id,
                        "method": request.method,
                        "path": request.url.path,
                        "error": err,
                        "duration_ms": round(process_time * 1000.0, 3),
                    }
                },
            )
            _emit_audit_console_pair(
                request,
                request_id,
                status_code=500,
                process_time_s=process_time,
                response=None,
                error=err,
                is_error=True,
            )
            raise

        process_time = time() - start_time
        duration_ms = round(process_time * 1000.0, 3)

        audit_logger.info(
            "http_request_complete",
            extra={
                "props": {
                    "event": "http_audit",
                    "phase": "complete",
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "query_params": dict(request.query_params),
                    "client": request.client.host if request.client else None,
                    "user_agent": request.headers.get("user-agent"),
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                    "response_content_type": response.headers.get("content-type"),
                    "response_content_length": response.headers.get("content-length"),
                }
            },
        )

        if _AUDIT_CONSOLE_MODE == "always":
            audit_summary_logger.info(
                _build_audit_out_line(
                    request,
                    request_id,
                    response.status_code,
                    process_time,
                    response=response,
                )
            )
        else:
            _emit_audit_console_pair(
                request,
                request_id,
                status_code=response.status_code,
                process_time_s=process_time,
                response=response,
                is_error=False,
            )

        response.headers["X-Request-ID"] = request_id
        return response
