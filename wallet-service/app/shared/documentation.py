from app.shared.response import ApiResponse
from fastapi import status

common_error_responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Unauthorized: Authentication required or invalid token.",
        "model": ApiResponse[None],
        "content": {
            "application/json": {
                "examples": {
                    "unauthorized": {
                        "summary": "Invalid or missing token",
                        "value": {"message": "Authentication failed: Invalid or missing token.", "data": None, "error": "AUTHENTICATION_ERROR"}
                    }
                }
            }
        }
    },
    status.HTTP_403_FORBIDDEN: {
        "description": "Forbidden: User does not have the necessary permissions (e.g., not an admin).",
        "model": ApiResponse[None],
        "content": {
            "application/json": {
                "examples": {
                    "forbidden": {
                        "summary": "Insufficient permissions",
                        "value": {"message": "Access denied: Admin role is required.", "data": None, "error": "AUTHORIZATION_ERROR"}
                    }
                }
            }
        }
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Not Found: The requested resource (user) was not found.",
        "model": ApiResponse[None],
        "content": {
            "application/json": {
                "examples": {
                    "user_not_found": {
                        "summary": "User not found",
                        "value": {"message": "User not found.", "data": None, "error": "RESOURCE_NOT_FOUND"}
                    }
                }
            }
        }
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal Server Error: An unexpected error occurred on the server.",
        "model": ApiResponse[None],
        "content": {
            "application/json": {
                "examples": {
                    "internal_error": {
                        "summary": "Server error",
                        "value": {"message": "An unexpected error occurred.", "data": None, "error": "INTERNAL_SERVER_ERROR"}
                    }
                }
            }
        }
    }
}



common_wallet_error_responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Unauthorized: Authentication required or invalid token.",
        "model": ApiResponse[None],
        "content": {
            "application/json": {
                "examples": {
                    "unauthorized": {
                        "summary": "Invalid or missing token",
                        "value": {"message": "Authentication failed: Invalid or missing token.", "data": None, "error": "AUTHENTICATION_ERROR"}
                    }
                }
            }
        }
    },
    status.HTTP_403_FORBIDDEN: {
        "description": "Forbidden: User does not have the necessary permissions (e.g., not an employee).",
        "model": ApiResponse[None],
        "content": {
            "application/json": {
                "examples": {
                    "forbidden": {
                        "summary": "Insufficient permissions",
                        "value": {"message": "Access denied: Employee role is required.", "data": None, "error": "AUTHORIZATION_ERROR"}
                    }
                }
            }
        }
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Not Found: The requested resource (wallet or user) was not found.",
        "model": ApiResponse[None],
        "content": {
            "application/json": {
                "examples": {
                    "resource_not_found": {
                        "summary": "Resource not found",
                        "value": {"message": "Wallet or User not found.", "data": None, "error": "RESOURCE_NOT_FOUND"}
                    }
                }
            }
        }
    },

    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal Server Error: An unexpected error occurred on the server.",
        "model": ApiResponse[None],
        "content": {
            "application/json": {
                "examples": {
                    "internal_error": {
                        "summary": "Server error",
                        "value": {"message": "An unexpected error occurred.", "data": None, "error": "INTERNAL_SERVER_ERROR"}
                    }
                }
            }
        }
    }
}
