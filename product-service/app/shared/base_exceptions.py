from typing import Any, Dict, Optional
from http import HTTPStatus


class DomainException(Exception):
    """
    Base class for all domain-specific exceptions.

    These exceptions represent business rule violations or issues originating
    from the core domain logic. They typically map to HTTP 4xx status codes,
    indicating client-side errors or invalid requests.
    """

    status_code: int = HTTPStatus.BAD_REQUEST  # Default status code for domain errors

    def __init__(
        self,
        message: str = "A domain-specific error occurred.",
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Initializes a new DomainException.

        Args:
            message (str): A human-readable message describing the error.
                           Defaults to "A domain-specific error occurred.".
            error_code (Optional[str]): A unique, programmatic code for the error.
                                        Defaults to the class name if not provided.
            details (Optional[Dict[str, Any]]): A dictionary for additional error context
                                               or specific data related to the error.
                                               Defaults to None.
        """
        self.message = message
        # Use class name as default error_code if not explicitly provided
        self.error_code = (
            error_code if error_code is not None else self.__class__.__name__.upper()
        )
        self.details = details if details is not None else {}
        super().__init__(self.message)


class ApplicationException(Exception):
    """
    Base class for all application-specific exceptions.

    These exceptions typically represent issues that arise within the application's
    infrastructure, data access layers, or external service integrations. They
    often map to HTTP 5xx status codes, indicating server-side problems.
    """

    status_code: int = (
        HTTPStatus.INTERNAL_SERVER_ERROR
    )  # Default status code for application errors

    def __init__(
        self,
        message: str = "An application error occurred.",
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Initializes a new ApplicationException.

        Args:
            message (str): A human-readable message describing the error.
                           Defaults to "An application error occurred.".
            error_code (Optional[str]): A unique, programmatic code for the error.
                                        Defaults to the class name if not provided.
            details (Optional[Dict[str, Any]]): A dictionary for additional error context
                                               or specific data related to the error.
                                               Defaults to None.
        """
        self.message = message
        # Use class name as default error_code if not explicitly provided
        self.error_code = (
            error_code if error_code is not None else self.__class__.__name__.upper()
        )
        self.details = details if details is not None else {}
        super().__init__(self.message)


class NotFoundException(ApplicationException):
    """
    Exception raised when a requested resource or entity cannot be found.

    This is an application-level exception as it often indicates an issue
    with data retrieval from the persistence layer, or an invalid ID provided
    by the client. Maps to HTTP 404 Not Found.
    """

    status_code: int = HTTPStatus.NOT_FOUND

    def __init__(self, entity_name: str, entity_id: Any):
        """
        Initializes a NotFoundException for a specific entity.

        Args:
            entity_name (str): The name of the entity that was not found (e.g., "Product", "User").
            entity_id (Any): The ID or identifier used to search for the entity.
        """
        message = f"{entity_name} with ID '{entity_id}' not found."
        error_code = f"{entity_name.upper()}_NOT_FOUND"
        details = {"entity": entity_name, "id": entity_id}
        super().__init__(message=message, error_code=error_code, details=details)


class ValidationException(DomainException):
    """
    Exception raised when input data fails validation rules.

    This is a domain-level exception as it indicates that the provided data
    does not conform to the expected structure or business constraints.
    Maps to HTTP 422 Unprocessable Entity.
    """

    status_code: int = HTTPStatus.UNPROCESSABLE_ENTITY

    def __init__(
        self,
        field: Optional[str] = None,
        reason: str = "Validation failed.",
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Initializes a ValidationException.

        Args:
            field (Optional[str]): The name of the specific field that failed validation.
                                   Defaults to None if the validation error is general.
            reason (str): A specific reason for the validation failure.
                          Defaults to "Validation failed.".
            details (Optional[Dict[str, Any]]): Additional context about the validation error.
                                               This can include a list of multiple errors.
                                               Defaults to None.
        """
        message = (
            f"Validation failed for field '{field}': {reason}" if field else reason
        )
        error_code = "VALIDATION_ERROR"

        # Merge field and reason into details, ensuring details is always a dict
        _details = {"reason": reason}
        if field:
            _details["field"] = field
        if details:
            _details.update(details)

        super().__init__(message=message, error_code=error_code, details=_details)


class DatabaseException(ApplicationException):
    """
    Exception raised for errors occurring during database operations.

    This is an application-level exception as it signifies issues with the
    persistence layer, such as connection problems, query failures, or
    database-specific errors. Maps to HTTP 503 Service Unavailable or
    HTTP 500 Internal Server Error, depending on the specific cause.
    """

    status_code: int = HTTPStatus.SERVICE_UNAVAILABLE  # Often used for temporary issues

    def __init__(
        self,
        message: str = "A database operation failed.",
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Initializes a DatabaseException.

        Args:
            message (str): A human-readable message describing the database error.
            error_code (Optional[str]): A programmatic code for the database error.
            details (Optional[Dict[str, Any]]): Additional context about the database error,
                                               e.g., specific error codes from the DB driver.
        """
        super().__init__(message=message, error_code=error_code, details=details)


class AuthorizationException(Exception):
    """Base class for all auth-specific exceptions."""

    status_code = HTTPStatus.UNAUTHORIZED

    def __init__(
        self,
        message: str = "A auth-specific error occurred.",
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details
        super().__init__(self.message)
