from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, List
from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"
    CUSTOMER = "customer"
    PREMUIM_CUSTOMER = "premuim_customer"
    MANAGER = "manager"


@dataclass
class User:
    id: str
    email: str
    phone: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    roles: List[UserRole] = []

    def __post_init__(self):
        if self.roles is None:
            self.roles = [UserRole.CUSTOMER]

    def is_deleted(self) -> bool:
        """Check if user is soft deleted"""
        return self.deleted_at is not None

    def has_role(self, role: UserRole) -> bool:
        """Check if user has a specific role"""
        return role in self.roles

    def is_admin(self) -> bool:
        """Check if user has admin role"""
        return self.has_role(UserRole.ADMIN)

    def is_active(self) -> bool:
        """Check if user is active (not deleted)"""
        return not self.is_deleted()

    def add_role(self, role: UserRole) -> None:
        """Add a role to the user"""
        if role not in self.roles:
            self.roles.append(role)

    def remove_role(self, role: UserRole) -> None:
        """Remove a role from the user"""
        if role in self.roles:
            self.roles.remove(role)

    def soft_delete(self) -> None:
        """Soft delete the user"""
        self.deleted_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def restore(self) -> None:
        """Restore a soft deleted user"""
        self.deleted_at = None
        self.updated_at = datetime.now(timezone.utc)

    def to_mongo_dict(self) -> dict:
        """Convert user to a dictionary suitable for MongoDB"""
        return {
            "_id": self.id,
            "email": self.email,
            "phone": self.phone,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
            "roles": [role.value for role in self.roles],
        }

    @classmethod
    def from_mongo_dict(cls, doc: dict) -> "User":
        """Create a User instance from a MongoDB document"""
        return cls(
            id=doc["_id"],
            email=doc["email"],
            phone=doc.get("phone", ""),
            created_at=doc["created_at"],
            updated_at=doc["updated_at"],
            deleted_at=doc.get("deleted_at"),
            roles=[UserRole(role) for role in doc.get("roles", [])],
        )
