from datetime import datetime, date
from sqlalchemy import Integer, String, Boolean, Date, DateTime, Enum as SqlEnum
from sqlalchemy.orm import mapped_column, Mapped
from app.users.domain.enums import UserRole, Gender
from app.users.domain.entities import User
from config.postgres_config import Base

class UserModel(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date)
    password: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole, name='role_enum', create_type=False), default=UserRole.CUSTOMER, nullable=False)
    gender: Mapped[Gender] = mapped_column(SqlEnum(Gender, name='gender_enum', create_type=False), default=Gender.OTHER,  nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False)
    
        
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
            hashed_password=self.password,
            is_active=self.is_active,
            created_at=created_at,
            updated_at=updated_at,
        )
        
    @classmethod
    def from_domain(cls, user: User) -> 'UserModel':
        """Create SQLAlchemy model from domain entity"""
        return cls(
            id=user.id if user.id != 0 else None,
            email=user.email,
            date_of_birth=user.date_of_birth,
            password=user.hashed_password,
            phone_number=user.phone_number,
            first_name=user.first_name,
            last_name=user.last_name,
            gender=user.gender,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        
    def update_from_domain(self, user: User):
        """Update SQLAlchemy model from domain entity"""
        self.email = user.email
        self.date_of_birth = user.date_of_birth
        self.password = user.hashed_password
        self.role = user.role
        self.is_active = user.is_active
        self.created_at = user.created_at
        self.updated_at = user.updated_at
