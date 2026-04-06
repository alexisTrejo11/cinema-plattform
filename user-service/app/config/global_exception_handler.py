import logging
from http import HTTPStatus
from typing import Any

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.shared.exceptions import (
    ApplicationException,
    AuthorizationException,
    DomainException,
)
from app.shared.response import error_json_response

logger = logging.getLogger("app")


def _normalize_details(details: Any) -> dict[str, Any]:
    """Coerce exception details into a dict for ErrorResponse.details."""
    if not details:
        return {}
    if isinstance(details, dict):
        return details
    if isinstance(details, list):
        return {"errors": details}
    return {"info": str(details)}


def _flatten_validation_errors(errors: list[dict]) -> list[dict[str, str]]:
    return [
        {
            "field": ".".join(str(loc) for loc in err.get("loc", ["unknown"])),
            "message": err.get("msg", "Validation error"),
        }
        for err in errors
    ]


def _detail_to_message(detail: Any) -> str:
    if isinstance(detail, str):
        return detail
    if isinstance(detail, list):
        parts: list[str] = []
        for item in detail:
            if isinstance(item, dict):
                parts.append(str(item.get("msg", item)))
            else:
                parts.append(str(item))
        return "; ".join(parts) if parts else "Request error"
    if isinstance(detail, dict):
        return str(detail.get("detail", detail))
    return str(detail)


def _code_for_http_status(status_code: int) -> str:
    return {
        HTTPStatus.BAD_REQUEST: "BAD_REQUEST",
        HTTPStatus.UNAUTHORIZED: "UNAUTHORIZED",
        HTTPStatus.FORBIDDEN: "FORBIDDEN",
        HTTPStatus.NOT_FOUND: "NOT_FOUND",
        HTTPStatus.CONFLICT: "CONFLICT",
        HTTPStatus.UNPROCESSABLE_ENTITY: "VALIDATION_ERROR",
        HTTPStatus.TOO_MANY_REQUESTS: "TOO_MANY_REQUESTS",
        HTTPStatus.INTERNAL_SERVER_ERROR: "INTERNAL_SERVER_ERROR",
        HTTPStatus.SERVICE_UNAVAILABLE: "SERVICE_UNAVAILABLE",
    }.get(status_code, f"HTTP_{status_code}")


async def handle_domain_exceptions(request: Request, exc: DomainException) -> Any:
    logger.warning(
        "Domain error [%s] %s | path=%s",
        exc.error_code,
        exc.message,
        request.url.path,
    )
    return error_json_response(
        status_code=exc.status_code,
        code=exc.error_code,
        message=exc.message,
        details=_normalize_details(exc.details),
    )


async def handle_application_exceptions(request: Request, exc: ApplicationException) -> Any:
    logger.error(
        "Application error [%s] %s | path=%s",
        exc.error_code,
        exc.message,
        request.url.path,
        exc_info=exc,
    )
    return error_json_response(
        status_code=exc.status_code,
        code=exc.error_code,
        message="An internal server error occurred.",
        details={},
    )


async def handle_auth_exceptions(request: Request, exc: AuthorizationException) -> Any:
    logger.warning(
        "Auth error [%s] %s | path=%s",
        exc.error_code,
        exc.message,
        request.url.path,
    )
    headers = (
        {"WWW-Authenticate": "Bearer"}
        if exc.status_code == HTTPStatus.UNAUTHORIZED
        else None
    )
    return error_json_response(
        status_code=exc.status_code,
        code=exc.error_code,
        message=exc.message,
        details=_normalize_details(exc.details),
        headers=headers,
    )


async def handle_pydantic_validation_errors(request: Request, exc: ValidationError) -> Any:
    flat = _flatten_validation_errors(exc.errors())
    logger.warning(
        "Pydantic validation error | path=%s | fields=%s",
        request.url.path,
        [d["field"] for d in flat],
    )
    return error_json_response(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        code="VALIDATION_ERROR",
        message="One or more fields failed validation.",
        details={"errors": flat},
    )


async def handle_path_validation_errors(request: Request, exc: RequestValidationError) -> Any:
    flat = _flatten_validation_errors(exc.errors())
    logger.warning(
        "Request validation error | path=%s | fields=%s",
        request.url.path,
        [d["field"] for d in flat],
    )
    return error_json_response(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        code="VALIDATION_ERROR",
        message="One or more fields failed validation.",
        details={"errors": flat},
    )


async def handle_db_exceptions(request: Request, exc: SQLAlchemyError) -> Any:
    logger.error(
        "Database error [%s] | path=%s",
        type(exc).__name__,
        request.url.path,
        exc_info=exc,
    )
    return error_json_response(
        status_code=HTTPStatus.SERVICE_UNAVAILABLE,
        code="DATABASE_ERROR",
        message="A database connection issue occurred. Please try again later.",
        details={},
    )


async def handle_http_exceptions(request: Request, exc: HTTPException) -> Any:
    """Normalize FastAPI/Starlette HTTPException (e.g. HTTPBearer, Depends) to ErrorResponse."""
    headers = dict(exc.headers) if exc.headers else None
    detail = exc.detail
    details: dict[str, Any] = {}
    message = _detail_to_message(detail)
    if (
        isinstance(detail, list)
        and detail
        and isinstance(detail[0], dict)
        and "loc" in detail[0]
    ):
        flat = _flatten_validation_errors(detail)  # type: ignore[arg-type]
        details["errors"] = flat
        message = "One or more fields failed validation."
    code = _code_for_http_status(exc.status_code)
    logger.warning(
        "HTTP error [%s] %s | path=%s",
        code,
        message,
        request.url.path,
    )
    return error_json_response(
        status_code=exc.status_code,
        code=code,
        message=message,
        details=details,
        headers=headers,
    )


async def handle_generic_exceptions(request: Request, exc: Exception) -> Any:
    logger.error(
        "Unhandled exception [%s] | path=%s",
        type(exc).__name__,
        request.url.path,
        exc_info=exc,
    )
    return error_json_response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred.",
        details={},
    )
