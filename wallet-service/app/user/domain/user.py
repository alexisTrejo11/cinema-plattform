from typing import Any, Dict, List, Optional
from datetime import datetime
from .value_objects import UserRole, UserId


class User:
    def __init__(
        self,
        id: "UserId",
        email: str,
        roles: List[UserRole],
        is_active: bool,
        created_at: Optional[datetime],
        updated_at: Optional[datetime],
        deleted_at: Optional[datetime],
    ) -> None:
        self.__id = id
        self.__email = email
        self.__roles = roles
        self.__is_active = is_active
        self.__created_at = created_at
        self.__updated_at = updated_at
        self.__deleted_at = deleted_at

    def get_id(self) -> "UserId":
        return self.__id

    def get_email(self) -> str:
        return self.__email

    def get_roles(self) -> List[UserRole]:
        return self.__roles

    def is_active(self) -> bool:
        return self.__is_active

    def get_created_at(self) -> Optional[datetime]:
        return self.__created_at

    def get_updated_at(self) -> Optional[datetime]:
        return self.__updated_at

    def get_deleted_at(self) -> Optional[datetime]:
        return self.__deleted_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.__id),
            "email": self.__email,
            "roles": [role.value for role in self.__roles],
            "is_active": self.__is_active,
            "created_at": self.__created_at.isoformat() if self.__created_at else None,
            "updated_at": self.__updated_at.isoformat() if self.__updated_at else None,
            "deleted_at": self.__deleted_at.isoformat() if self.__deleted_at else None,
        }
