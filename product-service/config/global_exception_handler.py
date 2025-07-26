from http import HTTPStatus
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import logging
from app.shared.base_exceptions import *
from app.shared.response import ApiResponse, ErrorResponse

from fastapi import FastAPI

logger = logging.getLogger("app")

app = FastAPI()


@app.exception_handler(DomainException)
async def handle_domain_exceptions(request: Request, exc: DomainException):
    error_response = ErrorResponse(
        code=exc.error_code,
        type=exc.__class__.__name__,
        message=exc.message,
        details=exc.details,
    )
    api_response = ApiResponse.failure(error=error_response, message=exc.message)
    return JSONResponse(status_code=exc.status_code, content=api_response.model_dump())


@app.exception_handler(ApplicationException)
async def handle_application_exceptions(request: Request, exc: ApplicationException):
    logger.error(f"Application error: {exc}", exc_info=exc)
    error_response = ErrorResponse(
        code=exc.error_code,
        type=exc.__class__.__name__,
        message=exc.message,
        details=exc.details,
    )
    api_response = ApiResponse.failure(
        error=error_response,
        message=f"An application error occurred: {exc.message}",  # Un mensaje más general
    )
    return JSONResponse(status_code=exc.status_code, content=api_response.model_dump())


@app.exception_handler(AuthorizationException)
async def handle_auth_exceptions(
    request: Request, exc: AuthorizationException
):  # Cambiado a AuthorizationException
    logger.error(f"Auth error: {exc}", exc_info=exc)
    error_response = ErrorResponse(
        code=exc.error_code,
        type=exc.__class__.__name__,
        message=exc.message,
        details=exc.details,
    )
    api_response = ApiResponse.failure(
        error=error_response, message=f"Authorization failed: {exc.message}"
    )
    return JSONResponse(status_code=exc.status_code, content=api_response.model_dump())


@app.exception_handler(ValidationError)
async def handle_pydantic_validation_errors(request: Request, exc: ValidationError):
    logger.warning(f"Pydantic validation error: {exc}", exc_info=exc)

    # Procesar los errores para obtener detalles estructurados
    errors_details = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error.get("loc", []))
        error_type = error.get("type", "invalid")
        message = error.get("msg", "Invalid value")

        errors_details.append(
            {
                "field": field if field else "request_body",
                "code": error_type.upper(),
                "message": message,
                "context": error.get("ctx", None),
            }
        )

    error_response = ErrorResponse(
        code="VALIDATION_FAILED",
        type="ValidationError",
        message="Invalid request data. Please check the errors and try again.",
        details=errors_details,
    )

    api_response = ApiResponse.failure(
        error=error_response, message="Validation error in request data"
    )

    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY, content=api_response.model_dump()
    )


@app.exception_handler(ValueError)
async def handle_value_errors(request: Request, exc: ValueError):
    logger.warning(f"ValueError: {exc}", exc_info=exc)

    error_response = ErrorResponse(
        code="INVALID_INPUT", type="ValueError", message=str(exc), details=[]
    )
    api_response = ApiResponse.failure(
        error=error_response, message="Invalid input provided."
    )
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST, content=api_response.model_dump()
    )


@app.exception_handler(Exception)
async def handle_generic_exceptions(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {exc}", exc_info=exc)

    error_response = ErrorResponse(
        code="INTERNAL_SERVER_ERROR",
        type="UnhandledException",
        message="An unexpected error occurred on the server.",
        details=None,
    )
    api_response = ApiResponse.failure(
        error=error_response, message="An internal server error occurred."
    )
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content=api_response.model_dump()
    )
