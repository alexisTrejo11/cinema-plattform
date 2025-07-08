from uuid import UUID
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from config.postgres_config import Base


class WalletModel(Base):
    """SQLAlchemy model for the wallets table using modern annotations."""

    __tablename__ = "cinem_wallets"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    balance: Mapped[float] = mapped_column(nullable=False, default=0.0)

    user: Mapped["UserModel"] = relationship(
        back_populates="wallets", lazy="selectin"  # Consider your loading strategy
    )


class UserModel(Base):
    """SQLAlchemy model for the users table using modern annotations."""

    __tablename__ = "cinem_wallets_users"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )

    wallets: Mapped[list["WalletModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
