from sqlalchemy.exc import IntegrityError
import pytest
from typing import Dict, Any
from datetime import datetime, timezone

from tests.users.conftest import *

from app.users.domain.entities import User
from app.users.domain.exceptions import UserAlreadyExistsException, UserNotFoundException
from app.users.domain.enums import UserRole

# -----------------------------
# Test: Create User
# -----------------------------
@pytest.mark.asyncio
async def test_create_user_successfully(user_repo: UserRepository, sample_user: User):
    """Tests that a user can be successfully created."""

    # Act
    created_user = await user_repo.create(sample_user)

    # Assert
    assert isinstance(created_user.id, int)
    assert created_user.id != 0
    assert created_user.email == sample_user.email
    assert created_user.phone_number == sample_user.phone_number
    assert created_user.hashed_password == sample_user.hashed_password
    assert created_user.first_name == sample_user.first_name
    assert created_user.last_name == sample_user.last_name
    assert created_user.date_of_birth == sample_user.date_of_birth
    assert created_user.role == sample_user.role
    assert created_user.is_active == sample_user.is_active
    assert isinstance(created_user.created_at, datetime)
    assert isinstance(created_user.updated_at, datetime)

    assert (datetime.now() - created_user.created_at).total_seconds() < 5
    assert (datetime.now() - created_user.updated_at).total_seconds() < 5


@pytest.mark.asyncio
async def test_create_user_email_already_exists(user_repo: UserRepository, sample_user: User):
    """Tests that creating a user with an existing email raises UserAlreadyExistsException."""
    # Arrange
    await user_repo.create(sample_user)

    duplicate_email_user_data = sample_user.model_dump()
    duplicate_email_user_data["phone_number"] = "1112223333" # same email
    duplicate_email_user = User(**duplicate_email_user_data)

    # Act & Assert
    with pytest.raises(IntegrityError):
        await user_repo.create(duplicate_email_user)
        

# -----------------------------
# Test: Get User by ID
# -----------------------------
@pytest.mark.asyncio
async def test_get_user_by_id_successfully(user_repo: UserRepository, sample_user: User):
    """Tests getting a user by their ID."""
    # Arrange
    created_user = await user_repo.create(sample_user)
    
    # Act
    fetched_user = await user_repo.get_by_id(created_user.id)
    # Assert
    assert fetched_user is not None
    assert fetched_user.id == created_user.id
    assert fetched_user.email == sample_user.email

@pytest.mark.asyncio
async def test_get_user_by_id_not_found(user_repo: UserRepository):
    """Tests getting a non-existent user by ID returns None."""
    # Act
    fetched_user = await user_repo.get_by_id(999999)
    # Assert
    assert fetched_user is None
