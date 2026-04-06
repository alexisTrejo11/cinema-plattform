"""OpenAPI / ReDoc fragments shared across routes.

``common_error_responses`` values are FastAPI ``responses=`` entries (not model instances).
401/403 use FastAPI's :class:`fastapi.HTTPException` shape ``{"detail": "..."}``.
Other codes use the same flat :class:`app.hared.core.response.ErrorResponse` as the global handlers.
"""

from typing import Any

from app.hared.core.response import ErrorResponse


def _error_response_spec(
    description: str,
    *,
    code: str,
    message: str,
    details: list[Any] | None = None,
) -> dict[str, Any]:
    return {
        "model": ErrorResponse,
        "description": description,
        "content": {
            "application/json": {
                "example": {
                    "code": code,
                    "message": message,
                    "details": details or [],
                }
            }
        },
    }


def _http_exception(description: str, detail: str) -> dict[str, Any]:
    return {
        "description": description,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {"detail": {"type": "string"}},
                    "required": ["detail"],
                },
                "example": {"detail": detail},
            }
        },
    }


common_error_responses: dict[int, dict[str, Any]] = {
    400: _error_response_spec(
        "Domain validation or bad request.",
        code="VALIDATION_ERROR",
        message="Validation failed for field 'min_amount': must be non-negative.",
        details=[{"field": "min_amount", "reason": "Must be >= 0"}],
    ),
    401: _http_exception(
        "Missing or invalid `Authorization: Bearer` token.",
        "Not authenticated.",
    ),
    403: _http_exception(
        "Authenticated user lacks permission for this operation (e.g. admin only).",
        "This action requires an admin role.",
    ),
    404: _error_response_spec(
        "Referenced resource does not exist.",
        code="PAYMENT_METHOD_NOT_FOUND",
        message="Payment Method with payment method id stripe-card-mx was not found.",
        details=[{"entity": "Payment Method", "id": "stripe-card-mx"}],
    ),
    422: _error_response_spec(
        "Request body or path/query parameters failed validation.",
        code="VALIDATION_ERROR",
        message="One or more fields failed validation.",
        details=[
            {"field": "body.name", "message": "Field required"},
        ],
    ),
    503: _error_response_spec(
        "Database or infrastructure failure.",
        code="DATABASE_ERROR",
        message="A database connection issue occurred. Please try again later.",
        details=[],
    ),
    500: _error_response_spec(
        "Unexpected server error.",
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred.",
        details=[],
    ),
}
