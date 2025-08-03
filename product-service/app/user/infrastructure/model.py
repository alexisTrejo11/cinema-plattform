import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from app.user.domain.user import UserRole
from config.db.postgres_config import Base
from app.user.domain.user import User, UserId


class UserSQLModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    roles: Mapped[List[UserRole]] = mapped_column(
        ARRAY(Enum(UserRole, name="user_role_enum")), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, onupdate=datetime.utcnow
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def __repr__(self):
        return f"<UserSQLModel(id={self.id}, email='{self.email}')>"

    def to_domain_user(self):

        return User(
            id=UserId(self.id),
            email=self.email,
            roles=[role for role in self.roles],
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
        )

    @staticmethod
    def from_domain(user: User) -> "UserSQLModel":
        return UserSQLModel(
            id=user.get_id().value,
            email=user.get_email(),
            roles=[role.value for role in user.get_roles()],
            is_active=user.is_active(),
            created_at=user.get_created_at(),
            updated_at=user.get_updated_at(),
            deleted_at=user.get_deleted_at(),
        )

    def update_from_domain(self, user: User) -> None:
        self.id = user.get_id().value
        self.email = user.get_email()
        self.roles = [role for role in user.get_roles()]
        self.is_active = user.is_active()
        self.updated_at = user.get_updated_at()
        self.deleted_at = user.get_deleted_at()
