import pytest
from datetime import datetime

from tests.users.conftest import *

from app.users.domain import User, UserRole


@pytest.mark.asyncio
async def test_save_user_successfully(user_repo: UserRepository, sample_user: User):
    created_user = await user_repo.save(sample_user)

    assert isinstance(created_user.id, int)
    assert created_user.id != 0
    assert created_user.email == sample_user.email
    assert created_user.phone_number == sample_user.phone_number
    assert created_user.password == sample_user.password
    assert created_user.first_name == sample_user.first_name
    assert created_user.last_name == sample_user.last_name
    assert created_user.date_of_birth == sample_user.date_of_birth
    assert created_user.role == sample_user.role
    assert created_user.status == sample_user.status
    assert isinstance(created_user.created_at, datetime)
    assert isinstance(created_user.updated_at, datetime)


@pytest.mark.asyncio
async def test_save_user_email_already_exists(user_repo: UserRepository, sample_user: User):
    await user_repo.save(sample_user)

    duplicate_email_user = sample_user.model_copy()
    duplicate_email_user.id = 0
    duplicate_email_user.phone_number = "1112223333"

    with pytest.raises(RuntimeError, match="Failed to save user"):
        await user_repo.save(duplicate_email_user)


@pytest.mark.asyncio
async def test_get_user_by_id_successfully(user_repo: UserRepository, sample_user: User):
    created_user = await user_repo.save(sample_user)

    fetched_user = await user_repo.get_by_id(created_user.id)
    assert fetched_user is not None
    assert fetched_user.id == created_user.id
    assert fetched_user.email == sample_user.email


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(user_repo: UserRepository):
    fetched_user = await user_repo.get_by_id(999999)
    assert fetched_user is None
