"""Shared OpenAPI / Swagger fragments for ticket HTTP routes."""

from typing import Any, Dict

# Standard HTTP error shapes (FastAPI default for 422; 429 from SlowAPI)
HTTP_422: Dict[str, Any] = {
    "description": "Request validation failed (body, path, or query parameters).",
    "content": {
        "application/json": {
            "example": {
                "detail": [
                    {
                        "type": "value_error",
                        "loc": ["body", "user_email"],
                        "msg": "value is not a valid email address",
                    }
                ]
            }
        }
    },
}

HTTP_429: Dict[str, Any] = {
    "description": "Rate limit exceeded for this client IP.",
    "content": {
        "application/json": {
            "example": {"detail": "Rate limit exceeded: 10 per 1 minute"}
        }
    },
}

HTTP_404_JSON: Dict[str, Any] = {
    "description": "Resource not found.",
    "content": {
        "application/json": {"example": {"detail": "Ticket not found"}}
    },
}

HTTP_400_JSON: Dict[str, Any] = {
    "description": "Business rule or state conflict.",
    "content": {
        "application/json": {
            "example": {"detail": "Cannot cancel already used ticket"}
        }
    },
}


def merge_responses(*blocks: Dict[str, Any]) -> Dict[str, Any]:
    """Merge OpenAPI response maps (later keys override)."""
    out: Dict[str, Any] = {}
    for b in blocks:
        out.update(b)
    return out


COMMON_TICKET_READ = {
    "422": HTTP_422,
    "429": HTTP_429,
}

COMMON_TICKET_WRITE = {
    "422": HTTP_422,
    "429": HTTP_429,
    "400": HTTP_400_JSON,
    "404": HTTP_404_JSON,
}

# PATCH endpoints that return 204 No Content
PATCH_NO_CONTENT = {
    "204": {"description": "Operation succeeded; no response body."},
    "400": HTTP_400_JSON,
    "404": HTTP_404_JSON,
    "422": HTTP_422,
    "429": HTTP_429,
}
