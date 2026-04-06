from datetime import datetime, date
from typing import Optional
from sqlalchemy import Integer, String, Date, DateTime, Enum as SqlEnum, BOOLEAN
from sqlalchemy.orm import mapped_column, Mapped
from app.users.domain import UserRole, Gender, Status, User
from app.config.postgres_config import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    date_of_birth: Mapped[date] = mapped_column(Date)
    password: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(255))
    totp_secret: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_2fa_enabled: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    last_name: Mapped[Optional[str]] = mapped_column(String(255))
    phone_number: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole, name="role_enum", create_type=False),
        default=UserRole.CUSTOMER,
        nullable=False,
    )
    gender: Mapped[Gender] = mapped_column(
        SqlEnum(Gender, name="gender_enum", create_type=False),
        default=Gender.OTHER,
        nullable=False,
    )
    status: Mapped[Status] = mapped_column(
        SqlEnum(Status, name="user_status_enum", create_type=False),
        default=Status.PENDING,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), nullable=False
    )

    def to_domain(self) -> User:
        """Convert SQLAlchemy model to domain entity"""
        created_at = self.created_at
        updated_at = self.updated_at

        return User(
            id=self.id,
            email=self.email,
            phone_number=self.phone_number,
            first_name=self.first_name,
            last_name=self.last_name,
            gender=self.gender,
            role=self.role,
            date_of_birth=self.date_of_birth,
            is_2fa_enabled=self.is_2fa_enabled,
            totp_secret=self.totp_secret,
            password=self.password,
            status=self.status,
            created_at=created_at,
            updated_at=updated_at,
        )

    @classmethod
    def from_domain(cls, user: User) -> "UserModel":
        """Create SQLAlchemy model from domain entity"""
        return cls(
            id=user.id if user.id != 0 else None,
            email=user.email,
            date_of_birth=user.date_of_birth,
            password=user.password,
            is_2fa_enabled=user.is_2fa_enabled,
            totp_secret=user.totp_secret,
            phone_number=user.phone_number,
            first_name=user.first_name,
            last_name=user.last_name,
            gender=user.gender,
            role=user.role,
            status=user.status,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def update_from_domain(self, user: User):
        """Update SQLAlchemy model from domain entity"""
        self.email = user.email
        self.date_of_birth = user.date_of_birth
        self.password = user.password
        self.role = user.role
        self.status = user.status
        self.is_2fa_enabled = user.is_2fa_enabled
        self.totp_secret = user.totp_secret
        self.created_at = user.created_at
        self.updated_at = user.updated_at
