from http import HTTPStatus
from fastapi import FastAPI, Request
from app.shared.base_exceptions import DomainException, ApplicationException, AuthorizationException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import logging

app = FastAPI()

@app.exception_handler(DomainException)
async def handle_domain_exceptions(request: Request, exc: DomainException):
    print(f"///////")
    print(f"Caught exception type: {type(exc)}")
    print(f"Is caught exception a DomainException (from handler's perspective)? {isinstance(exc, HandlerDomainException)}")
    print(f"ID of HandlerDomainException: {id(HandlerDomainException)}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )
from app.shared.base_exceptions import ApplicationException as HandlerDomainException

@app.exception_handler(ApplicationException)
async def handle_application_exceptions(request: Request, exc: ApplicationException):
    logging.error(f"Application error: {exc}", exc_info=exc)
    
    print(f"Caught exception type: {type(exc)}")
    print(f"Is caught exception a DomainException (from handler's perspective)? {isinstance(exc, HandlerDomainException)}")
    print(f"ID of HandlerDomainException: {id(HandlerDomainException)}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )

@app.exception_handler(AuthorizationException)
async def handle_auth_exceptions(request: Request, exc: ApplicationException):
    logging.error(f"Auth error: {exc}", exc_info=exc)
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )


@app.exception_handler(ValidationError)
async def handle_pydantic_validation_errors(request: Request, exc: ValidationError):
    """
    Handles Pydantic validation errors, typically from request body parsing.
    Provides structured error details for client-side consumption.
    """
    logging.warning(f"Pydantic validation error: {exc}", exc_info=exc)
    
    errors_details = []
    for error in exc.errors():
        # 'loc' provides the path to the field (e.g., ('body', 'field_name'))
        field = ".".join(map(str, error.get('loc', ['unknown_field'])))
        message = error.get('msg', 'Validation error')
        errors_details.append({"field": field, "message": message})

    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "One or more validation errors occurred in the request data.",
                "details": errors_details
            }
        }
    )

@app.exception_handler(ValueError)
async def handle_value_errors(request: Request, exc: ValueError):
    """
    Handles generic ValueError exceptions. These often arise from invalid input
    or business logic that cannot proceed with a given value.
    """
    logging.warning(f"ValueError: {exc}", exc_info=exc)
    
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={
            "error": {
                "code": "INVALID_INPUT",
                "message": str(exc), 
                "details": []
            }
        }
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



GLOBAL_EXCEPTION_HANDLERS = {
    DomainException: handle_domain_exceptions,
    ApplicationException: handle_application_exceptions,
    AuthorizationException: handle_auth_exceptions,
    ValidationError: handle_pydantic_validation_errors,
    ValueError: handle_value_errors,
    Exception: handle_generic_exceptions
}