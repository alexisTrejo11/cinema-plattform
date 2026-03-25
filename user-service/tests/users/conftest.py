from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Any, Dict

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import *  # noqa: F401,F403

from app.users.domain import Gender, Status, User, UserRole
from app.users.infrastructure.persistence.sqlalch_user_repo import (
    SQLAlchemyUserRepository as UserRepository,
)


@pytest.fixture
def sample_user_data() -> Dict[str, Any]:
    return {
        "id": 0,
        "email": f"testuser_{uuid.uuid4().hex[:8]}@example.com",
        "phone_number": "1234567890",
        "password": "TestPass1!x",
        "first_name": "John",
        "last_name": "Doe",
        "gender": Gender.MALE,
        "date_of_birth": date(1990, 1, 1),
        "role": UserRole.CUSTOMER,
        "status": Status.ACTIVE,
        "created_at": datetime(2024, 1, 1, 12, 0, 0),
        "updated_at": datetime(2024, 1, 2, 12, 0, 0),
    }


@pytest.fixture
def sample_user(sample_user_data: Dict[str, Any]) -> User:
    return User(**sample_user_data)


@pytest.fixture
def another_sample_user(sample_user_data: Dict[str, Any]) -> User:
    data = sample_user_data.copy()
    data["email"] = f"another_testuser_{uuid.uuid4().hex[:8]}@example.com"
    data["phone_number"] = "9876543210"
    data["first_name"] = "Jane"
    data["last_name"] = "Smith"
    return User(**data)


@pytest.fixture
def updated_user_data() -> Dict[str, Any]:
    return {
        "email": f"updated_email_{uuid.uuid4().hex[:8]}@example.com",
        "phone_number": "5551112222",
        "first_name": "Johnny",
        "last_name": "Depp",
        "status": Status.INACTIVE,
        "role": UserRole.ADMIN,
    }


@pytest_asyncio.fixture(scope="function")
async def user_repo(session: AsyncSession) -> UserRepository:
    return UserRepository(session)
