from typing import Any, Optional, TypeVar, Generic
from pydantic import BaseModel, Field

T = TypeVar('T')

class Result(Generic[T]):
    """
    A generic class to encapsulate the outcome of an operation,
    indicating success or failure and holding either data or an error message.

    This class is useful for functions that might succeed with a value
    or fail with an explanation, providing a more explicit return type
    than raising exceptions for expected failure scenarios.

    Type parameter:
        T: The type of the data held in case of a successful outcome.
    """
    def __init__(self, success: bool, data: Optional[T] = None, error: Optional[str] = None):
        """
        Initializes a new instance of the Result class.

        Args:
            success (bool): True if the operation was successful, False otherwise.
            data (Optional[T]): The data returned by the operation if successful.
                                 Defaults to None.
            error (Optional[str]): An error message if the operation failed.
                                   Defaults to None.
        """
        self._success = success
        self._data = data
        self._error = error

    def is_success(self) -> bool:
        """
        Checks if the operation represented by this Result was successful.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self._success

    def get_error_message(self) -> Optional[str]:
        """
        Retrieves the error message if the operation failed.

        Returns:
            Optional[str]: The error message, or None if the operation was successful.
        """
        return self._error

    def get_data(self) -> T:
        """
        Retrieves the data if the operation was successful.

        Returns:
            Optional[T]: The data, or None if the operation failed.
        """
        if self._data:
            return self._data
        else:
            raise ValueError("No data on Result")
    
    @staticmethod
    def success(data: Optional[Any] = None) -> 'Result':
        """
        Creates a new Result instance representing a successful outcome.

        Args:
            data (Optional[Any]): The data to be associated with the successful result.
                                  Defaults to None.

        Returns:
            Result: A Result instance indicating success.
        """

        return Result[Any](success=True, data=data)

    @staticmethod
    def error(error_message: str) -> 'Result':
        """
        Creates a new Result instance representing a failed outcome.

        Args:
            error_message (str): The error message explaining the failure.

        Returns:
            Result: A Result instance indicating failure.
        """
        return Result[Any](success=False, error=error_message)

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the Result instance to a dictionary representation.

        Returns:
            dict[str, Any]: A dictionary containing 'success', 'data', and 'error' keys.
        """
        return {"success": self._success, "data": self._data, "error": self._error}

    def __repr__(self) -> str:
        """
        Returns a string representation of the Result instance for debugging.
        """
        return f"Result(success={self._success}, data={self._data}, error={self._error})"
    

class ErrorResponse(BaseModel): 
    """
    Represents a structured error response, typically used within an API response.

    This Pydantic model provides clear fields for common error attributes,
    making error handling consistent across an application.
    """
    code: Optional[str] = Field(
        None,
        description="An optional, machine-readable error code (e.g., 'AUTH_FAILED', 'INVALID_INPUT', 'USER_NOT_FOUND').",
        examples=["INVALID_INPUT", "USER_ALREADY_EXISTS"]
    )
    type: Optional[str] = Field(
        None,
        description="An optional, human-readable type or category of the error (e.g., 'AuthenticationError', 'ValidationError', 'NotFoundError').",
        examples=["ValidationError", "AuthenticationError"]
    )
    message: Optional[str] = Field(
        None,
        description="A human-readable message describing the error. This message is usually displayed to the end-user.",
        examples=["Invalid email format.", "User with this email already exists.", "Invalid credentials."]
    )

    class Config:
        """
        Pydantic configuration for the ErrorResponse model.
        """
        json_schema_extra = {
            "example": {
                "code": "VALIDATION_ERROR",
                "type": "InputError",
                "message": "The provided email address is invalid."
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
        examples=[True, False]
    )
    data: Optional[T] = Field(
        None,
        description="The payload data returned by the API if the request was successful. Its type is determined by the generic type parameter T. This field will be null if `is_success` is false."
    )
    message: str = Field(
        '',
        description="A human-readable message providing context about the API response (e.g., 'User created successfully', 'Operation failed due to invalid data').",
        examples=["User created successfully.", "Failed to retrieve data.", "Item updated."]
    )
    error: Optional[ErrorResponse] = Field(
        None,
        description="Details of the error if `is_success` is false. This field will be null if `is_success` is true."
    )

    class Config:
        """
        Pydantic configuration for the ApiResponse model.
        """
        json_schema_extra = {
            "examples": [
                {
                    "is_success": True,
                    "data": {"id": 1, "first_name": "John", "email": "john@example.com"},
                    "message": "User retrieved successfully.",
                    "error": None
                },
                {
                    "is_success": False,
                    "data": None,
                    "message": "Failed to create user due to validation errors.",
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "type": "InputError",
                        "message": "Email already registered."
                    }
                }
            ]
        }

    @staticmethod
    def success(data: Optional[T] = None, message: str = '') -> 'ApiResponse[T]':
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
            error=None
        )
        
    @staticmethod
    def failure(error: ErrorResponse, message: str = '') -> 'ApiResponse[Any]':
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
            is_success=False,
            data=None,
            message=message,
            error=error
        )