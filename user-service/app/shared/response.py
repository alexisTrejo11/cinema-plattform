from typing import Any, Optional

class Result:
    def __init__(self, success: bool, data: Optional[Any] = None, error: Optional[str] = None):
        self._success = success
        self._data = data
        self._error = error

    def is_success(self) -> bool:
        return self._success

    def get_error_message(self) -> Optional[str]:
        return self._error

    def get_data(self) -> Optional[Any]:
        return self._data if self._success else None
    
    @staticmethod
    def success(data: Optional[Any] = None) -> 'Result':
        return Result(success=True, data=data)

    @staticmethod
    def error(error_message: str) -> 'Result':
        return Result(success=False, error=error_message)

    def to_dict(self) -> dict[str, Any]:
        return {"success": self._success, "data": self._data, "error": self._error}

    def __repr__(self) -> str:
        return f"Result(success={self._success}, data={self._data}, error={self._error})"