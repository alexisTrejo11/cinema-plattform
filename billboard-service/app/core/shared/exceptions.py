from typing import Optional, Dict, Any
from http import HTTPStatus

class DomainException(Exception):
    """Base class for all domain-specific exceptions."""
    status_code = HTTPStatus.BAD_REQUEST
    
    def __init__(
        self,
        message: str = "A domain-specific error occurred.",
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details
        super().__init__(self.message)

class ApplicationException(Exception):
    """Base class for all application-specific exceptions."""
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR 
    
    def __init__(
        self,
        message: str = "An application error occurred.",
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details
        super().__init__(self.message)


class NotFoundException(DomainException):
    status_code = HTTPStatus.NOT_FOUND
    
    def __init__(self, entity: str, entity_id: Any):
        super().__init__(
            message=f"{entity} with ID {entity_id} not found",
            error_code=f"{entity.upper()}_NOT_FOUND",
            details={"entity": entity, "id": entity_id}
        )

class ValidationException(DomainException):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    
    def __init__(self, field: str, reason: str):
        super().__init__(
            message=f"Validation failed for field '{field}'",
            error_code="VALIDATION_ERROR",
            details={"field": field, "reason": reason}
        )

class DatabaseException(ApplicationException):
    status_code = HTTPStatus.SERVICE_UNAVAILABLE