from uuid import UUID
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"
    CUSTOMER = "CUSTOMER"


class UserId:
    def __init__(self, value: UUID) -> None:
        self.value = value

    @classmethod
    def from_string(cls, value: str) -> "UserId":
        return cls(UUID(value))

    def to_string(self) -> str:
        return str(self.value)
