from tests.conftest import * 
import pytest
import pytest_asyncio
from typing import Dict, Any
from datetime import date
import uuid

from app.users.domain import User, UserRole
from app.users.infrastructure.persistence.sql_alchemy_user_repo import SQLAlchemyUserRepository as UserRepository


@pytest.fixture
def sample_user_data() -> Dict[str, Any]:
    """Provides a dictionary of user data for creating a domain User entity."""
    # Note: 'id' will be set by the DB upon creation, so we don't include it here initially.
    # The 'hashed_password' is what your domain User entity expects.
    return {
        "id" : 0,
        "email": f"testuser_{uuid.uuid4().hex[:8]}@example.com", # Unique email for each test
        "phone_number": "1234567890",
        "hashed_password": "supersecurehash", # Your User domain model expects hashed_password
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": date(1990, 1, 1),
        "role": UserRole.CUSTOMER,
        "is_active": True,
    }

@pytest.fixture
def sample_user(sample_user_data: Dict[str, Any]) -> User:
    """Provides a sample User domain entity."""
    return User(**sample_user_data)

@pytest.fixture
def another_sample_user(sample_user_data: Dict[str, Any]) -> User:
    """Provides another distinct sample User domain entity."""
    data = sample_user_data.copy()
    data["email"] = f"another_testuser_{uuid.uuid4().hex[:8]}@example.com"
    data["phone_number"] = "9876543210" 
    data["first_name"] = "Jane"
    data["last_name"] = "Smith"
    return User(**data)

@pytest.fixture
def updated_user_data() -> Dict[str, Any]:
    """Provides a dictionary of data to update a user."""
    return {
        "email": f"updated_email_{uuid.uuid4().hex[:8]}@example.com",
        "phone_number": "5551112222",
        "first_name": "Johnny",
        "last_name": "Depp",
        "is_active": False,
        "role": UserRole.ADMIN,
    }

@pytest_asyncio.fixture(scope="function")
async def user_repo(session: AsyncSession) -> UserRepository:
    """Provides an instance of the UserRepository for testing."""
    return UserRepository(session)