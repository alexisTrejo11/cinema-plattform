from typing import Any
from app.shared.base_exceptions import NotFoundException

class UserNotFoundException(NotFoundException):
    """Exception raised when a user is not found in the repository."""

    def __init__(self, entity_id: Any):
        super().__init__("User", entity_id)