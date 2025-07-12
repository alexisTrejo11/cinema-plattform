from sqlalchemy import String, Boolean, DateTime, Enum, ARRAY
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from datetime import datetime
import uuid
from typing import List, Optional

from app.user.domain.user import UserRole

Base = declarative_base()


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
        from app.user.domain.user import User, UserId

        return User(
            id=UserId(self.id),
            email=self.email,
            roles=[role for role in self.roles],
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
        )
