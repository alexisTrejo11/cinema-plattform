from typing import Any, Optional, TypeVar, Generic, Dict
from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorResponse(BaseModel):
    code: Optional[str] = Field(
        None, description="An optional, machine-readable error code"
    )
    type: Optional[str] = Field(
        None, description="An optional, human-readable type or category of the error"
    )
    message: Optional[str] = Field(
        None, description="A human-readable message describing the error"
    )
    details: Optional[Any] = Field(
        None, description="Additional details about the error, e.g., validation errors"
    )  # Agregamos 'details' para ser consistente

    class Config:
        json_schema_extra = {
            "example": {
                "code": "VALIDATION_ERROR",
                "type": "InputError",
                "message": "The provided email address is invalid.",
            }
        }


class ApiResponse(BaseModel, Generic[T]):
    """
    A generic Pydantic model for standardizing all API responses, whether successful or failed.

    This class encapsulates the common structure of an API response,
    including a success indicator, optional data payload, a contextual message,
    and structured error details when an operation fails.

    Type parameter:
        T: The expected type of the `data` field when the API call is successful.
           This allows `ApiResponse` to be type-checked with specific data models.
    """

    is_success: bool = Field(
        ...,
        description="Indicates whether the API request was successful (true) or failed (false).",
        examples=[True, False],
    )
    data: Optional[T] = Field(
        None,
        description="The payload data returned by the API if the request was successful. Its type is determined by the generic type parameter T. This field will be null if `is_success` is false.",
    )
    message: str = Field(
        "",
        description="A human-readable message providing context about the API response (e.g., 'User created successfully', 'Operation failed due to invalid data').",
        examples=[
            "User created successfully.",
            "Failed to retrieve data.",
            "Item updated.",
        ],
    )
    error: Optional[ErrorResponse] = Field(
        None,
        description="Details of the error if `is_success` is false. This field will be null if `is_success` is true.",
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata about the API response, such as pagination info.",
    )

    class Config:
        """
        Pydantic configuration for the ApiResponse model.
        """

        json_schema_extra = {
            "examples": [
                {
                    "is_success": True,
                    "data": {
                        "id": 1,
                        "first_name": "John",
                        "email": "john@example.com",
                    },
                    "message": "User retrieved successfully.",
                    "error": None,
                },
                {
                    "is_success": False,
                    "data": None,
                    "message": "Failed to create user due to validation errors.",
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "type": "InputError",
                        "message": "Email already registered.",
                    },
                },
            ]
        }

    @staticmethod
    def success(
        data: Optional[T] = None,
        message: str = "",
        metadata: Optional[Dict[str, Any]] = {},
    ) -> "ApiResponse[T]":
        """
        Creates a new `ApiResponse` instance for a successful API response.

        Args:
            data (Optional[T]): The data payload for the successful response. Defaults to None.
            message (str): A message indicating the success. Defaults to an empty string.

        Returns:
            ApiResponse[T]: A successful API response instance.
        """
        return ApiResponse(
            is_success=True,
            data=data,
            message=message,
            error=None,
            metadata=metadata if metadata is not None else None,
        )

    @staticmethod
    def failure(
        error: ErrorResponse,
        message: str = "error",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "ApiResponse[Any]":
        """
        Creates a new `ApiResponse` instance for a failed API response.

        Args:
            error (ErrorResponse): The structured error details.
            message (str): A message indicating the failure. Defaults to an empty string.

        Returns:
            ApiResponse[Any]: A failed API response instance. Note: `Any` is used for `T`
                             as there is typically no specific `data` type on failure,
                             allowing the generic `ApiResponse` to be used for error responses
                             regardless of the expected success data type.
        """
        return ApiResponse(
            is_success=False, data=None, message=message, error=error, metadata=metadata
        )
