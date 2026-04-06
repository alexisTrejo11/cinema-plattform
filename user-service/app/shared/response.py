from typing import Any, Optional, TypeVar, Generic

from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


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

    def __init__(
        self, success: bool, data: Optional[T] = None, error: Optional[str] = None
    ):
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
    def success(data: Optional[Any] = None) -> "Result":
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
    def error(error_message: str) -> "Result":
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
        return (
            f"Result(success={self._success}, data={self._data}, error={self._error})"
        )


class ErrorResponse(BaseModel):
    """
    Represents a structured error response, typically used within an API response.

    This Pydantic model provides clear fields for common error attributes,
    making error handling consistent across an application.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": "VALIDATION_ERROR",
                "message": "The provided email address is invalid.",
                "details": {"field": "email", "reason": "Invalid email format."},
            }
        }
    )

    code: Optional[str] = Field(
        None,
        description="An optional, machine-readable error code (e.g., 'AUTH_FAILED', 'INVALID_INPUT', 'USER_NOT_FOUND').",
        examples=["INVALID_INPUT", "USER_ALREADY_EXISTS"],
    )
    message: Optional[str] = Field(
        None,
        description="A human-readable message describing the error. This message is usually displayed to the end-user.",
        examples=[
            "Invalid email format.",
            "User with this email already exists.",
            "Invalid credentials.",
        ],
    )
    details: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional details about the error, providing more context or specific information.",
        examples=[
            {"field": "email", "reason": "Invalid email format."},
            {"field": "password", "reason": "Password is too short."},
        ],
    )


def error_json_response(
    status_code: int,
    *,
    code: Optional[str] = None,
    message: Optional[str] = None,
    details: Optional[dict[str, Any]] = None,
    headers: Optional[dict[str, str]] = None,
) -> JSONResponse:
    """
    Build a JSON HTTP response whose body matches ErrorResponse (same shape everywhere).
    """
    body = ErrorResponse(
        code=code,
        message=message,
        details=details if details is not None else {},
    ).model_dump(mode="json")
    return JSONResponse(status_code=status_code, content=body, headers=headers)


class InformativeResponse(BaseModel):
    """
    Represents a structured information response,
    typically used as ouput to inform the user about the result of an
    operation when the success could be different from the expected one.
    """

    message: str = Field(
        ...,
        description="A human-readable message describing the information.",
        examples=[
            "User created successfully.",
            "User updated successfully.",
            "User deleted successfully.",
        ],
    )
