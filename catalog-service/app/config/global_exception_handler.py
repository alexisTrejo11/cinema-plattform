import logging
from typing import Any

from http import HTTPStatus
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.shared.core.exceptions import (
    applicationException,
    AuthorizationException,
    DomainException,
)
from app.shared.core.response import ErrorResponse

logger = logging.getLogger("app")


def _error_response(
    status_code: int, code: str, message: str, details: list | None = None
) -> JSONResponse:
    body = ErrorResponse(
        code=code,
        message=message,
        details=details or [],
    ).model_dump(mode="json")
    return JSONResponse(status_code=status_code, content=body)


def _normalize_details(details) -> list:
    """Coerce exception details (dict, list, or None) into a list for the response."""
    if not details:
        return []
    if isinstance(details, list):
        return details
    if isinstance(details, dict):
        return [details]
    return [{"info": str(details)}]


def _flatten_validation_errors(errors: list[dict]) -> list[dict]:
    """Turn Pydantic / FastAPI error dicts into flat {field, message} items."""
    return [
        {
            "field": ".".join(str(loc) for loc in err.get("loc", ["unknown"])),
            "message": err.get("msg", "Validation error"),
        }
        for err in errors
    ]


# ─── Domain (4xx — safe to expose to clients) ────────────────────────


async def handle_domain_exceptions(request: Request, exc: DomainException):
    logger.warning(
        "Domain error [%s] %s | path=%s",
        exc.error_code,
        exc.message,
        request.url.path,
    )
    return _error_response(
        status_code=exc.status_code,
        code=exc.error_code,
        message=exc.message,
        details=_normalize_details(exc.details),
    )


# ─── application (5xx — internal details hidden) ─────────────────────


async def handle_application_exceptions(request: Request, exc: applicationException):
    logger.error(
        "application error [%s] %s | path=%s",
        exc.error_code,
        exc.message,
        request.url.path,
        exc_info=exc,
    )
    return _error_response(
        status_code=exc.status_code,
        code=exc.error_code,
        message="An internal server error occurred.",
    )


# ─── Authorization ───────────────────────────────────────────────────


async def handle_auth_exceptions(request: Request, exc: AuthorizationException):
    logger.warning(
        "Auth error [%s] %s | path=%s",
        exc.error_code,
        exc.message,
        request.url.path,
    )
    return _error_response(
        status_code=exc.status_code,
        code=exc.error_code,
        message=exc.message,
        details=_normalize_details(exc.details),
    )


# ─── Validation (Pydantic + FastAPI path/query) ──────────────────────


async def handle_pydantic_validation_errors(request: Request, exc: ValidationError):
    details = _flatten_validation_errors(exc.errors())
    logger.warning(
        "Pydantic validation error | path=%s | fields=%s",
        request.url.path,
        [d["field"] for d in details],
    )
    return _error_response(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        code="VALIDATION_ERROR",
        message="One or more fields failed validation.",
        details=details,
    )


async def handle_path_validation_errors(request: Request, exc: RequestValidationError):
    details = _flatten_validation_errors(exc.errors())
    logger.warning(
        "Request validation error | path=%s | fields=%s",
        request.url.path,
        [d["field"] for d in details],
    )
    return _error_response(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        code="VALIDATION_ERROR",
        message="One or more fields failed validation.",
        details=details,
    )


# ─── Database (SQLAlchemy — details hidden, logged in full) ──────────


async def handle_db_exceptions(request: Request, exc: SQLAlchemyError):
    logger.error(
        "Database error [%s] | path=%s",
        type(exc).__name__,
        request.url.path,
        exc_info=exc,
    )
    return _error_response(
        status_code=HTTPStatus.SERVICE_UNAVAILABLE,
        code="DATABASE_ERROR",
        message="A database connection issue occurred. Please try again later.",
    )


# ─── Catch-all ────────────────────────────────────────────────────────


async def handle_generic_exceptions(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception [%s] | path=%s",
        type(exc).__name__,
        request.url.path,
        exc_info=exc,
    )
    return _error_response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred.",
    )


exception_handlers: Any = {
    DomainException: handle_domain_exceptions,
    applicationException: handle_application_exceptions,
    AuthorizationException: handle_auth_exceptions,
    ValidationError: handle_pydantic_validation_errors,
    RequestValidationError: handle_path_validation_errors,
    SQLAlchemyError: handle_db_exceptions,
    Exception: handle_generic_exceptions,
}

GLOBAL_EXCEPTION_HANDLERS = exception_handlers
