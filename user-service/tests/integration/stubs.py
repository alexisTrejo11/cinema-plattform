"""Test doubles for integration tests."""

from __future__ import annotations

from datetime import date, datetime

from app.users.domain import User, UserRole, Gender, Status


def make_domain_user(
    *,
    user_id: int = 0,
    email: str = "integration@example.com",
    role: UserRole = UserRole.CUSTOMER,
) -> User:
    return User(
        id=user_id,
        email=email,
        password="TestPass1!x",
        phone_number="1234567890",
        first_name="Integration",
        last_name="User",
        gender=Gender.MALE,
        date_of_birth=date(1990, 5, 15),
        role=role,
        status=Status.ACTIVE,
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        updated_at=datetime(2024, 1, 2, 12, 0, 0),
    )
