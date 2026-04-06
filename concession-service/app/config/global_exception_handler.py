import logging
from http import HTTPStatus
from fastapi import FastAPI

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.shared.base_exceptions import (
    ApplicationException,
    AuthorizationException,
    DomainException,
)

logger = logging.getLogger("app")

app = FastAPI()


def _error_response(
    status_code: int, code: str, message: str, details: list | None = None
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message, "details": details or []}},
    )


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


@app.exception_handler(ApplicationException)
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


# ─── Application (5xx — internal details hidden) ─────────────────────


@app.exception_handler(ApplicationException)
async def handle_application_exceptions(request: Request, exc: ApplicationException):
    logger.error(
        "Application error [%s] %s | path=%s",
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


@app.exception_handler(AuthorizationException)
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


@app.exception_handler(ValidationError)
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


@app.exception_handler(RequestValidationError)
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


@app.exception_handler(SQLAlchemyError)
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


@app.exception_handler(Exception)
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
