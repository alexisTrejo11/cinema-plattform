from http import HTTPStatus
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import logging
from app.shared.base_exceptions import *
from app.shared.response import ApiResponse, ErrorResponse
from fastapi.exceptions import RequestValidationError

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
        message=f"An application error occurred",
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=api_response.model_dump(),
        headers={
            "X-Error-Type": exc.__class__.__name__,
            "X-Error-Code": exc.error_code,
        },
    )


@app.exception_handler(AuthorizationException)
async def handle_auth_exceptions(request: Request, exc: AuthorizationException):
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


@app.exception_handler(RequestValidationError)
async def handle_path_validation_errors(request: Request, exc: RequestValidationError):
    """Special handler for path parameter validation errors"""
    logger.warning(
        f"Path validation error on {request.url}: {str(exc)}",
        exc_info=True,
        extra={"validation_error": exc.errors(), "path_params": request.path_params},
    )

    errors_details = []
    for error in exc.errors():
        if error.get("type") == "uuid_parsing":
            field = error.get("loc", ["unknown"])[-1]
            input_value = error.get("input", "")
            ctx_error = error.get("ctx", {}).get("error", "")

            errors_details.append(
                {
                    "field": field,
                    "code": "INVALID_UUID_FORMAT",
                    "message": f"Invalid UUID format for {field}: {ctx_error}",
                    "expected_format": "8-4-4-4-12 hex digits (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)",
                    "received_value": input_value,
                    "correction": "Ensure you're using a properly formatted UUID string",
                }
            )
        else:
            field = ".".join(str(part) for part in error.get("loc", []))
            errors_details.append(
                {
                    "field": field,
                    "code": (
                        f"INVALID_{field.upper()}" if field else "INVALID_PATH_PARAM"
                    ),
                    "message": error.get("msg", "Invalid path parameter"),
                    "received_value": error.get("input"),
                    "expected_type": error.get("type", "").replace("_", " ").title(),
                }
            )

    error_response = ErrorResponse(
        code="INVALID_PATH_PARAMETERS",
        type="PathValidationError",
        message="One or more path parameters are invalid",
        details=errors_details,
    )

    api_response = ApiResponse.failure(
        error=error_response,
        message="Invalid path parameters in URL",
        metadata={
            "path": request.url.path,
            "method": request.method,
            "attempted_parameters": request.path_params,
        },
    )

    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content=api_response.model_dump(exclude_none=True),
        headers={
            "X-Error-Type": "PathValidation",
            "X-Error-Count": str(len(errors_details)),
        },
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
