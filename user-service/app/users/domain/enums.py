from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"
    EMPLOYEE = "EMPLOYEE"
    MANAGER = "MANAGER"


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class Status(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BANNED = "BANNED"


__all__ = [
    "UserRole",
    "Gender",
    "Status",
]
