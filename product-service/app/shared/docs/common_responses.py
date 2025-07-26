from app.shared.response import ApiResponse
from fastapi import status

common_error_responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Unauthorized: Authentication required or invalid token.",
        "model": ApiResponse[None],
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "UNAUTHORIZED",
                        "type": "Authentication Error",
                        "message": "Authentication failed: Invalid or missing token.",
                        "details": None,
                    },
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
    status.HTTP_403_FORBIDDEN: {
        "description": "Forbidden: User does not have the necessary permissions (e.g., not an admin).",
        "model": ApiResponse[None],
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "FORBIDDEN",
                        "type": "Authorization Error",
                        "message": "Access denied: Admin role is required.",
                        "details": None,
                    },
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal Server Error: An unexpected error occurred on the server.",
        "model": ApiResponse[None],
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "INTERNAL_SERVER_ERROR",
                        "type": "UnhandledException",
                        "message": "An unexpected error occurred on the server.",
                        "details": None,
                    },
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
}


common_public_error_responses = {
    status.HTTP_400_BAD_REQUEST: {
        "description": "Bad Request: The request was invalid or cannot be served.",
        "model": ApiResponse[None],
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "INVALID_HTTP_BODY",
                        "type": "Validation Error",
                        "message": "Request data is invalid or malformed.",
                        "details": None,
                    },
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal Server Error: An unexpected error occurred on the server.",
        "model": ApiResponse[None],
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "INTERNAL_SERVER_ERROR",
                        "type": "UnhandledException",
                        "message": "An unexpected error occurred on the server.",
                        "details": None,
                    },
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
}
