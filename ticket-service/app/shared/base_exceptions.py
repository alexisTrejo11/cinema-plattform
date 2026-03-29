from __future__ import annotations

from http import HTTPStatus
from typing import Any
from uuid import UUID

from app.shared.core.exceptions import DomainException


class NotFoundException(DomainException):
    def __init__(self, entity_name: str, entity_id: Any, id_name: str = "id"):
        sid = str(entity_id)
        super().__init__(
            f"{entity_name} with {id_name} {sid} was not found.",
            error_code=f"{entity_name.upper()}_NOT_FOUND",
            status_code=HTTPStatus.NOT_FOUND,
            details={"entity": entity_name, "id": sid},
        )


class ValidationException(DomainException):
    def __init__(self, field: str, reason: str):
        super().__init__(
            f"Validation failed for field '{field}': {reason}",
            error_code="VALIDATION_ERROR",
            status_code=HTTPStatus.BAD_REQUEST,
            details={"field": field, "reason": reason},
        )


class ConflictException(DomainException):
    def __init__(self, message: str, *, details: dict | None = None):
        super().__init__(
            message,
            error_code="CONFLICT",
            status_code=HTTPStatus.CONFLICT,
            details=details or {},
        )
