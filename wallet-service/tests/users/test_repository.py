import pytest
import pytest_asyncio
from typing import Dict, Any, List
from datetime import datetime, timezone
import uuid

from app.user.domain.user import User, UserRole, UserId
from app.user.infrastructure.sql_user_respository import SqlAlchemyUserRepository
from app.user.infrastructure.model import (
    UserSQLModel,
)

from tests.conftest import session


@pytest.fixture
def sample_user_data() -> Dict[str, Any]:
    """Provides a dictionary of user data for creating a domain User entity."""
    return {
        "id": UserId(uuid.uuid4()),
        "email": f"testuser_{uuid.uuid4().hex[:8]}@example.com",
        "roles": [UserRole.CUSTOMER, UserRole.MANAGER],
        "is_active": True,
        "created_at": datetime.now(timezone.utc).replace(tzinfo=None),
        "updated_at": datetime.now(timezone.utc).replace(tzinfo=None),
    }


@pytest.fixture
def sample_user(sample_user_data: Dict[str, Any]) -> User:
    """Provides a sample User domain entity."""
    return User(**sample_user_data)


@pytest.fixture
def another_sample_user_data() -> Dict[str, Any]:
    """Provides another distinct dictionary of user data."""
    return {
        "id": UserId(uuid.uuid4()),
        "email": f"another_testuser_{uuid.uuid4().hex[:8]}@example.com",
        "roles": [UserRole.CUSTOMER],
        "is_active": False,
        "created_at": datetime.now(timezone.utc).replace(tzinfo=None),
        "updated_at": datetime.now(timezone.utc).replace(tzinfo=None),
    }


@pytest.fixture
def another_sample_user(another_sample_user_data: Dict[str, Any]) -> User:
    """Provides another distinct sample User domain entity."""
    return User(**another_sample_user_data)


@pytest.fixture
def admin_user_data() -> Dict[str, Any]:
    """Provides a dictionary for an admin user."""
    return {
        "id": UserId(uuid.uuid4()),
        "email": f"admin_user_{uuid.uuid4().hex[:8]}@example.com",
        "roles": [UserRole.ADMIN],
        "is_active": True,
        "created_at": datetime.now(timezone.utc).replace(tzinfo=None),
        "updated_at": datetime.now(timezone.utc).replace(tzinfo=None),
    }


@pytest.fixture
def updated_user_data_for_save() -> Dict[str, Any]:
    """Provides a dictionary of data to update a user via save method."""
    return {
        "email": f"updated_email_{uuid.uuid4().hex[:8]}@example.com",
        "is_active": False,
        "roles": [UserRole.ADMIN],  # Changed from 'role' to 'roles' for consistency
    }


@pytest_asyncio.fixture(scope="function")
async def user_repo(session) -> SqlAlchemyUserRepository:
    """Provides an instance of the SqlAlchemyUserRepository for testing."""
    return SqlAlchemyUserRepository(session)


# --- Test Cases ---
@pytest.mark.asyncio
async def test_create_user_successfully(
    user_repo: SqlAlchemyUserRepository, sample_user_data: Dict[str, Any]
):
    """Tests that a user can be successfully saved (created)."""
    # Act
    created_user = await user_repo.save(sample_user_data)

    # Assert
    assert isinstance(created_user.get_id(), UserId)
    assert created_user.get_id().value == sample_user_data["id"].value
    assert created_user.get_email() == sample_user_data["email"]
    assert created_user.is_active() == sample_user_data["is_active"]
    assert created_user.get_roles() == sample_user_data["roles"]
    assert isinstance(created_user.get_created_at(), datetime)
    assert isinstance(created_user.get_updated_at(), datetime)

    # Check if timestamps are close to now (within a few seconds)
    now_utc_naive = datetime.now(timezone.utc).replace(tzinfo=None)
    assert (now_utc_naive - created_user.get_created_at()).total_seconds() < 5
    assert (now_utc_naive - created_user.get_updated_at()).total_seconds() < 5

    # Verify directly from DB (optional, but good for repository tests)
    db_user = await user_repo.session.get(UserSQLModel, created_user.get_id().value)
    assert db_user is not None
    assert db_user.email == sample_user_data["email"]
    assert db_user.is_active == sample_user_data["is_active"]
    assert db_user.roles == sample_user_data["roles"]


@pytest.mark.asyncio
async def test_get_by_id_found(
    user_repo: SqlAlchemyUserRepository, sample_user_data: Dict[str, Any]
):
    """Tests retrieving a user by ID when it exists."""
    # Arrange: Save a user first
    saved_user = await user_repo.save(sample_user_data)
    await user_repo.session.commit()  # Commit to make it queryable in a new session/transaction if needed

    # Act
    retrieved_user = await user_repo.get_by_id(str(saved_user.get_id().value))

    # Assert
    assert retrieved_user is not None
    assert retrieved_user.get_id().value == saved_user.get_id().value
    assert retrieved_user.get_email() == saved_user.get_email()


@pytest.mark.asyncio
async def test_get_by_id_not_found(user_repo: SqlAlchemyUserRepository):
    """Tests retrieving a user by ID when it does not exist."""
    # Act
    non_existent_id = str(uuid.uuid4())
    retrieved_user = await user_repo.get_by_id(non_existent_id)

    # Assert
    assert retrieved_user is None


@pytest.mark.asyncio
async def test_get_by_email_found(
    user_repo: SqlAlchemyUserRepository, sample_user_data: Dict[str, Any]
):
    """Tests retrieving a user by email when it exists."""
    # Arrange: Save a user first
    saved_user = await user_repo.save(sample_user_data)
    await user_repo.session.commit()

    # Act
    retrieved_user = await user_repo.get_by_email(saved_user.get_email())

    # Assert
    assert retrieved_user is not None
    assert retrieved_user.get_id().value == saved_user.get_id().value
    assert retrieved_user.get_email() == saved_user.get_email()


@pytest.mark.asyncio
async def test_get_by_email_not_found(user_repo: SqlAlchemyUserRepository):
    """Tests retrieving a user by email when it does not exist."""
    # Act
    non_existent_email = "nonexistent@example.com"
    retrieved_user = await user_repo.get_by_email(non_existent_email)

    # Assert
    assert retrieved_user is None


@pytest.mark.asyncio
async def test_update_user_successfully(
    user_repo: SqlAlchemyUserRepository,
    sample_user_data: Dict[str, Any],
    updated_user_data_for_save: Dict[str, Any],
):
    """Tests that an existing user can be successfully updated via save."""
    # Arrange: Create a user first
    original_user = await user_repo.save(sample_user_data)
    await user_repo.session.commit()

    # Prepare update data with the original user's ID
    update_data = updated_user_data_for_save.copy()
    update_data["id"] = original_user.get_id()  # Ensure the ID is passed for update

    # Act
    updated_user = await user_repo.save(update_data)

    # Assert the returned user is updated
    assert updated_user is not None
    assert (
        updated_user.get_id().value == original_user.get_id().value
    )  # ID should remain same
    assert updated_user.get_email() == update_data["email"]
    assert updated_user.is_active() == update_data["is_active"]
    assert updated_user.get_roles() == update_data["roles"]
    assert (
        updated_user.get_updated_at() > original_user.get_updated_at()
    )  # Updated timestamp should be newer

    # Verify directly from DB
    db_user = await user_repo.session.get(UserSQLModel, original_user.get_id().value)
    assert db_user is not None
    assert db_user.email == update_data["email"]
    assert db_user.is_active == update_data["is_active"]
    assert db_user.roles == update_data["roles"]


@pytest.mark.asyncio
async def test_list_all_users(
    user_repo: SqlAlchemyUserRepository,
    sample_user_data: Dict[str, Any],
    another_sample_user_data: Dict[str, Any],
    admin_user_data: Dict[str, Any],
):
    """Tests listing all users without any filters."""
    # Arrange: Save multiple users
    await user_repo.save(sample_user_data)
    await user_repo.save(another_sample_user_data)
    await user_repo.save(admin_user_data)
    await user_repo.session.commit()

    # Act
    users = await user_repo.list({})

    # Assert
    assert len(users) == 3
    # Check if all expected users are present by their IDs
    expected_ids = {
        sample_user_data["id"].value,
        another_sample_user_data["id"].value,
        admin_user_data["id"].value,
    }
    actual_ids = {user.get_id().value for user in users}
    assert expected_ids == actual_ids


@pytest.mark.asyncio
async def test_list_filter_by_is_active(
    user_repo: SqlAlchemyUserRepository,
    sample_user_data: Dict[str, Any],  # is_active: True
    another_sample_user_data: Dict[str, Any],  # is_active: False
):
    """Tests listing users filtered by is_active status."""
    # Arrange
    await user_repo.save(sample_user_data)
    await user_repo.save(another_sample_user_data)
    await user_repo.session.commit()

    # Act 1: Filter active users
    active_users = await user_repo.list({"is_active": True})
    # Assert 1
    assert len(active_users) == 1
    assert active_users[0].get_id().value == sample_user_data["id"].value

    # Act 2: Filter inactive users
    inactive_users = await user_repo.list({"is_active": False})
    # Assert 2
    assert len(inactive_users) == 1
    assert inactive_users[0].get_id().value == another_sample_user_data["id"].value


@pytest.mark.asyncio
async def test_list_filter_by_email_contains(
    user_repo: SqlAlchemyUserRepository,
    sample_user_data: Dict[str, Any],  # e.g., testuser_abc@example.com
    another_sample_user_data: Dict[str, Any],  # e.g., another_testuser_xyz@example.com
    admin_user_data: Dict[str, Any],  # e.g., admin_user_123@example.com
):
    """Tests listing users filtered by email substring (case-insensitive)."""
    # Arrange
    await user_repo.save(sample_user_data)
    await user_repo.save(another_sample_user_data)
    await user_repo.save(admin_user_data)
    await user_repo.session.commit()

    # Act: Search for "testuser" (should find both sample_user_data and another_sample_user_data)
    users_containing_test = await user_repo.list({"email_contains": "testuser"})
    assert len(users_containing_test) == 2
    found_ids = {user.get_id().value for user in users_containing_test}
    assert sample_user_data["id"].value in found_ids
    assert another_sample_user_data["id"].value in found_ids

    # Act: Search for "admin" (should find admin_user_data)
    users_containing_admin = await user_repo.list({"email_contains": "admin"})
    assert len(users_containing_admin) == 1
    assert users_containing_admin[0].get_id().value == admin_user_data["id"].value

    # Act: Search for "example.com" (should find all)
    users_containing_domain = await user_repo.list({"email_contains": "example.com"})
    assert len(users_containing_domain) == 3


@pytest.mark.asyncio
async def test_list_filter_by_role(
    user_repo: SqlAlchemyUserRepository,
    sample_user_data: Dict[str, Any],  # Roles: CUSTOMER, MANAGER
    another_sample_user_data: Dict[str, Any],  # Roles: CUSTOMER
    admin_user_data: Dict[str, Any],  # Roles: ADMIN
):
    """Tests listing users filtered by a specific role."""
    # Arrange
    await user_repo.save(sample_user_data)
    await user_repo.save(another_sample_user_data)
    await user_repo.save(admin_user_data)
    await user_repo.session.commit()

    # Act 1: Filter by CUSTOMER role (should find sample_user and another_sample_user)
    customer_users = await user_repo.list({"role": UserRole.CUSTOMER})
    assert len(customer_users) == 2
    customer_ids = {u.get_id().value for u in customer_users}
    assert sample_user_data["id"].value in customer_ids
    assert another_sample_user_data["id"].value in customer_ids

    # Act 2: Filter by MANAGER role (should find only sample_user)
    manager_users = await user_repo.list({"role": UserRole.MANAGER})
    assert len(manager_users) == 1
    assert manager_users[0].get_id().value == sample_user_data["id"].value

    # Act 3: Filter by ADMIN role (should find only admin_user)
    admin_users = await user_repo.list({"role": UserRole.ADMIN})
    assert len(admin_users) == 1
    assert admin_users[0].get_id().value == admin_user_data["id"].value


@pytest.mark.asyncio
async def test_list_pagination_limit_offset(
    user_repo: SqlAlchemyUserRepository,
    sample_user_data: Dict[str, Any],
    another_sample_user_data: Dict[str, Any],
    admin_user_data: Dict[str, Any],
):
    """Tests pagination (limit and offset) for user listing."""
    # Arrange: Save users, ensuring a predictable order for pagination tests
    # We'll use email for sorting to ensure consistent results
    users_to_save = [sample_user_data, another_sample_user_data, admin_user_data]
    # Sort by email for consistent pagination results
    users_to_save.sort(key=lambda x: x["email"])

    for user_data in users_to_save:
        await user_repo.save(user_data)
    await user_repo.session.commit()

    # Act 1: Limit 2, Offset 0
    users_page1 = await user_repo.list({"limit": 2, "offset": 0, "sort_by": "email"})
    assert len(users_page1) == 2
    assert users_page1[0].get_email() == users_to_save[0]["email"]
    assert users_page1[1].get_email() == users_to_save[1]["email"]

    # Act 2: Limit 2, Offset 1
    users_page2 = await user_repo.list({"limit": 2, "offset": 1, "sort_by": "email"})
    assert len(users_page2) == 2
    assert users_page2[0].get_email() == users_to_save[1]["email"]
    assert users_page2[1].get_email() == users_to_save[2]["email"]

    # Act 3: Limit 1, Offset 2
    users_page3 = await user_repo.list({"limit": 1, "offset": 2, "sort_by": "email"})
    assert len(users_page3) == 1
    assert users_page3[0].get_email() == users_to_save[2]["email"]

    # Act 4: Limit 1, Offset 3 (should be empty)
    users_page_empty = await user_repo.list(
        {"limit": 1, "offset": 3, "sort_by": "email"}
    )
    assert len(users_page_empty) == 0


@pytest.mark.asyncio
async def test_list_sort_by_email_asc_desc(
    user_repo: SqlAlchemyUserRepository,
    sample_user_data: Dict[str, Any],
    another_sample_user_data: Dict[str, Any],
    admin_user_data: Dict[str, Any],
):
    """Tests sorting users by email in ascending and descending order."""
    # Arrange: Save users
    users_to_save = [sample_user_data, another_sample_user_data, admin_user_data]
    for user_data in users_to_save:
        await user_repo.save(user_data)
    await user_repo.session.commit()

    # Expected sorted emails
    expected_emails_asc = sorted([u["email"] for u in users_to_save])
    expected_emails_desc = sorted([u["email"] for u in users_to_save], reverse=True)

    # Act 1: Sort ascending
    users_asc = await user_repo.list({"sort_by": "email", "sort_direction": "asc"})
    actual_emails_asc = [u.get_email() for u in users_asc]
    assert actual_emails_asc == expected_emails_asc

    # Act 2: Sort descending
    users_desc = await user_repo.list({"sort_by": "email", "sort_direction": "desc"})
    actual_emails_desc = [u.get_email() for u in users_desc]
    assert actual_emails_desc == expected_emails_desc


@pytest.mark.asyncio
async def test_delete_user_successfully(
    user_repo: SqlAlchemyUserRepository, sample_user_data: Dict[str, Any]
):
    """Tests deleting an existing user."""
    # Arrange: Save a user to delete
    saved_user = await user_repo.save(sample_user_data)
    await user_repo.session.commit()

    # Act
    delete_successful = await user_repo.delete(str(saved_user.get_id().value))

    # Assert
    assert delete_successful is True

    # Verify user is no longer in the database
    retrieved_user = await user_repo.get_by_id(str(saved_user.get_id().value))
    assert retrieved_user is None


@pytest.mark.asyncio
async def test_delete_user_not_found(user_repo: SqlAlchemyUserRepository):
    """Tests deleting a non-existent user."""
    # Act
    non_existent_id = str(uuid.uuid4())
    delete_successful = await user_repo.delete(non_existent_id)

    # Assert
    assert delete_successful is False
