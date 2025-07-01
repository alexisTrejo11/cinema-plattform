from http import HTTPStatus
from fastapi import FastAPI, Request
from app.utils.exceptions import DomainException, ApplicationException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import logging
from app.utils.response import ApiResponse, ErrorResponse

app = FastAPI()

@app.exception_handler(DomainException)
async def handle_domain_exceptions(request: Request, exc: DomainException):
    logging.error(f"error: {exc}", exc_info=exc)

    error_reponse = ApiResponse.failure(ErrorResponse(code=exc.error_code, type='Domain', details=exc.details), exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content=error_reponse.model_dump()
    )

@app.exception_handler(ApplicationException)
async def handle_application_exceptions(request: Request, exc: ApplicationException):
    logging.error(f"Application error: {exc}", exc_info=exc)
    
    error_reponse = ApiResponse.failure(ErrorResponse(code=exc.error_code, type='Application', details=exc.details), exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content=error_reponse.model_dump()
    )

@app.exception_handler(ValidationError)
async def handle_pydantic_validation_errors(request: Request, exc: ValidationError):
    """
    Handles Pydantic validation errors, typically from request body parsing.
    Provides structured error details for client-side consumption.
    """
    logging.warning(f"Pydantic validation error: {exc}", exc_info=exc)
    
    errors_details = {}
    for error in exc.errors():
        # 'loc' provides the path to the field (e.g., ('body', 'field_name'))
        field = ".".join(map(str, error.get('loc', ['unknown_field'])))
        message = error.get('msg', 'Validation error')
        errors_details[field] = message

    error_resonse = ApiResponse.failure(ErrorResponse(code="DATA_FORMAT_ERROR", type='Data Validation', details=errors_details), "One or more validation errors occurred in the request data.")
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content=error_resonse.model_dump()
    )

@app.exception_handler(ValueError)
async def handle_value_errors(request: Request, exc: ValueError):
    """
    Handles generic ValueError exceptions. These often arise from invalid input
    or business logic that cannot proceed with a given value.
    """
    logging.warning(f"ValueError: {exc}", exc_info=exc)
    
    error_response = ApiResponse.failure(ErrorResponse(code="INVALID_INPUT", type='Value Error', details={}), str(exc))
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content=error_response.model_dump()
    )


@app.exception_handler(Exception)
async def handle_generic_exceptions(request: Request, exc: Exception):
    logging.error(f"Unexpected error: {exc}", exc_info=exc)
    
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred"
            }
        }
    )
