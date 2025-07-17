import pytest
import pytest_asyncio
from typing import Dict, Any, List
from datetime import datetime, timezone
import uuid

from app.user.domain.user import User, UserRole, UserId
from app.user.infrastructure.sql_user_respository import SqlAlchemyUserRepository
from app.user.infrastructure.model import UserSQLModel
from app.user.domain.exceptions import UserNotFoundException
from tests.conftest import session


class SampleUserFixtures:
    """
    A collection of pytest fixtures for generating sample user data and domain entities.
    """

    @pytest.fixture(scope="class")
    def sample_user_data(self) -> Dict[str, Any]:
        """Provides a dictionary of user data for creating a domain User entity."""
        return {
            "id": UserId(uuid.uuid4()),
            "email": f"testuser_{uuid.uuid4().hex[:8]}@example.com",
            "roles": [UserRole.CUSTOMER, UserRole.MANAGER],
            "is_active": True,
            "created_at": datetime.now(timezone.utc).replace(tzinfo=None),
            "updated_at": datetime.now(timezone.utc).replace(tzinfo=None),
        }

    @pytest.fixture(scope="class")
    def sample_user(self, sample_user_data: Dict[str, Any]) -> User:
        """Provides a sample User domain entity."""
        return User(**sample_user_data)

    @pytest.fixture(scope="class")
    def another_sample_user_data(self) -> Dict[str, Any]:
        """Provides another distinct dictionary of user data."""
        return {
            "id": UserId(uuid.uuid4()),
            "email": f"another_testuser_{uuid.uuid4().hex[:8]}@example.com",
            "roles": [UserRole.CUSTOMER],
            "is_active": False,
            "created_at": datetime.now(timezone.utc).replace(tzinfo=None),
            "updated_at": datetime.now(timezone.utc).replace(tzinfo=None),
        }

    @pytest.fixture(scope="class")
    def another_sample_user(self, another_sample_user_data: Dict[str, Any]) -> User:
        """Provides another distinct sample User domain entity."""
        return User(**another_sample_user_data)

    @pytest.fixture(scope="class")
    def admin_user_data(self) -> Dict[str, Any]:
        """Provides a dictionary for an admin user."""
        return {
            "id": UserId(uuid.uuid4()),
            "email": f"admin_user_{uuid.uuid4().hex[:8]}@example.com",
            "roles": [UserRole.ADMIN],
            "is_active": True,
            "created_at": datetime.now(timezone.utc).replace(tzinfo=None),
            "updated_at": datetime.now(timezone.utc).replace(tzinfo=None),
        }

    @pytest.fixture(scope="class")
    def admin_user(self, admin_user_data: Dict[str, Any]) -> User:
        """Provides a sample Admin User domain entity."""
        return User(**admin_user_data)

    @pytest.fixture(scope="class")
    def updated_user_data_for_update_scenario(self) -> Dict[str, Any]:
        """Provides a dictionary of data to update a user via save method."""
        return {
            # ID will be added in the test from the original user
            "email": f"updated_email_{uuid.uuid4().hex[:8]}@example.com",
            "is_active": False,
            "roles": [UserRole.ADMIN, UserRole.MANAGER],
        }


@pytest_asyncio.fixture(scope="function")
async def user_repo(session) -> SqlAlchemyUserRepository:
    """Provides an instance of the SqlAlchemyUserRepository for testing."""
    return SqlAlchemyUserRepository(session)


# --- Test Cases ---
class TestUserRepository(SampleUserFixtures):  # Inherit from your fixture class
    @pytest.mark.asyncio
    async def test_create_user_successfully(
        self,
        user_repo: SqlAlchemyUserRepository,
        sample_user: User,  # Use the User object directly
    ):
        """Tests that a user can be successfully created."""
        # Act
        await user_repo.create(sample_user)

        # Assert: Fetch the user back from the DB to verify creation
        created_user = await user_repo.get_by_id(
            sample_user.get_id(), raise_exception=False
        )

        assert created_user is not None
        assert isinstance(created_user.get_id(), UserId)
        assert created_user.get_id().value == sample_user.get_id().value
        assert created_user.get_email() == sample_user.get_email()
        assert created_user.is_active() == sample_user.is_active()
        assert created_user.get_roles() == sample_user.get_roles()
        assert isinstance(created_user.get_created_at(), datetime)
        assert isinstance(created_user.get_updated_at(), datetime)

        # Check if timestamps are close to now (within a few seconds)
        now_utc_naive = datetime.now(timezone.utc).replace(tzinfo=None)
        assert (now_utc_naive - created_user.get_created_at()).total_seconds() < 5
        assert (now_utc_naive - created_user.get_updated_at()).total_seconds() < 5

        # Verify directly from DB (optional, but good for repository tests)
        db_user = await user_repo.session.get(UserSQLModel, created_user.get_id().value)
        assert db_user is not None
        assert db_user.email == sample_user.get_email()
        assert db_user.is_active == sample_user.is_active()
        assert db_user.roles == sample_user.get_roles()

    @pytest.mark.asyncio
    async def test_get_by_id_found(
        self,
        user_repo: SqlAlchemyUserRepository,
        sample_user: User,  # Use the User object directly
    ):
        """Tests retrieving a user by ID when it exists."""
        # Arrange: Create a user first
        await user_repo.create(sample_user)
        await user_repo.session.commit()

        # Act
        retrieved_user = await user_repo.get_by_id(
            sample_user.get_id()
        )  # Pass UserId object directly

        # Assert
        assert retrieved_user is not None
        assert retrieved_user.get_id().value == sample_user.get_id().value
        assert retrieved_user.get_email() == sample_user.get_email()

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, user_repo: SqlAlchemyUserRepository):
        """Tests retrieving a user by ID when it does not exist."""
        # Act
        non_existent_id = UserId(uuid.uuid4())  # Use UserId object
        retrieved_user = await user_repo.get_by_id(
            non_existent_id, raise_exception=False
        )

        # Assert
        assert retrieved_user is None

    @pytest.mark.asyncio
    async def test_get_by_email_found(
        self,
        user_repo: SqlAlchemyUserRepository,
        sample_user: User,  # Use the User object directly
    ):
        """Tests retrieving a user by email when it exists."""
        # Arrange: Create a user first
        await user_repo.create(sample_user)
        await user_repo.session.commit()

        # Act
        retrieved_user = await user_repo.get_by_email(sample_user.get_email())

        # Assert
        assert retrieved_user is not None
        assert retrieved_user.get_id().value == sample_user.get_id().value
        assert retrieved_user.get_email() == sample_user.get_email()

    @pytest.mark.asyncio
    async def test_get_by_email_not_found(self, user_repo: SqlAlchemyUserRepository):
        """Tests retrieving a user by email when it does not exist."""
        # Act
        non_existent_email = "nonexistent@example.com"
        retrieved_user = await user_repo.get_by_email(non_existent_email)

        # Assert
        assert retrieved_user is None

    @pytest.mark.asyncio
    async def test_update_user_successfully(
        self,
        user_repo: SqlAlchemyUserRepository,
        sample_user: User,  # Initial user for creation
        updated_user_data_for_update_scenario: Dict[str, Any],  # Data for updates
    ):
        """Tests that an existing user can be successfully updated."""
        # Arrange: Create a user first
        await user_repo.create(sample_user)
        await user_repo.session.commit()

        # Prepare a new User object with updated data and the original ID
        # This will be passed to the update method
        user_to_update = User(
            id=sample_user.get_id(),  # Use the ID of the existing user
            email=updated_user_data_for_update_scenario["email"],
            roles=updated_user_data_for_update_scenario["roles"],
            is_active=updated_user_data_for_update_scenario["is_active"],
            created_at=sample_user.get_created_at(),  # Keep original created_at
            updated_at=datetime.now(timezone.utc).replace(
                tzinfo=None
            ),  # Set new updated_at
        )

        # Act
        await user_repo.update(user_to_update)  # Changed from .save() to .update()

        # Assert: Fetch the user back from the DB to verify update
        returned_updated_user = await user_repo.get_by_id(user_to_update.get_id())

        assert returned_updated_user is not None
        assert (
            returned_updated_user.get_id().value == sample_user.get_id().value
        )  # ID should remain same
        assert (
            returned_updated_user.get_email()
            == updated_user_data_for_update_scenario["email"]
        )
        assert (
            returned_updated_user.is_active()
            == updated_user_data_for_update_scenario["is_active"]
        )
        assert (
            returned_updated_user.get_roles()
            == updated_user_data_for_update_scenario["roles"]
        )
        assert (
            returned_updated_user.get_updated_at() > sample_user.get_updated_at()
        )  # Updated timestamp should be newer

        # Verify directly from DB (optional, but good for repository tests)
        db_user = await user_repo.session.get(UserSQLModel, sample_user.get_id().value)
        assert db_user is not None
        assert db_user.email == updated_user_data_for_update_scenario["email"]
        assert db_user.is_active == updated_user_data_for_update_scenario["is_active"]
        assert db_user.roles == updated_user_data_for_update_scenario["roles"]

    @pytest.mark.asyncio
    async def test_update_user_not_found_raises_exception(
        self,
        user_repo: SqlAlchemyUserRepository,
        sample_user: User,  # Use as a template for a non-existent user
    ):
        """Tests that update raises UserNotFoundException when the user to update is not found."""
        # Arrange: Create a user object that does not exist in DB
        non_existent_user_id = UserId(uuid.uuid4())
        user_to_update_non_existent = User(
            id=non_existent_user_id,
            email="nonexistent@example.com",
            roles=[UserRole.CUSTOMER],
            is_active=True,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None),
            updated_at=datetime.now(timezone.utc).replace(tzinfo=None),
        )

        # Act & Assert
        with pytest.raises(UserNotFoundException) as exc_info:
            await user_repo.update(user_to_update_non_existent)

        assert str(non_existent_user_id.value) in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_list_all_users(
        self,
        user_repo: SqlAlchemyUserRepository,
        sample_user: User,
        another_sample_user: User,
        admin_user: User,
    ):
        """Tests listing all users without any filters."""
        # Arrange: Create multiple users
        await user_repo.create(sample_user)
        await user_repo.create(another_sample_user)
        await user_repo.create(admin_user)
        await user_repo.session.commit()

        # Act
        users = await user_repo.search({})

        # Assert
        assert len(users) == 3
        expected_ids = {
            sample_user.get_id().value,
            another_sample_user.get_id().value,
            admin_user.get_id().value,
        }
        actual_ids = {user.get_id().value for user in users}
        assert expected_ids == actual_ids

    @pytest.mark.asyncio
    async def test_list_filter_by_is_active(
        self,
        user_repo: SqlAlchemyUserRepository,
        sample_user: User,  # is_active: True
        another_sample_user: User,  # is_active: False
    ):
        """Tests listing users filtered by is_active status."""
        # Arrange
        await user_repo.create(sample_user)
        await user_repo.create(another_sample_user)
        await user_repo.session.commit()

        # Act 1: Filter active users
        active_users = await user_repo.search({"is_active": True})
        # Assert 1
        assert len(active_users) == 1
        assert active_users[0].get_id().value == sample_user.get_id().value

        # Act 2: Filter inactive users
        inactive_users = await user_repo.search({"is_active": False})
        # Assert 2
        assert len(inactive_users) == 1
        assert inactive_users[0].get_id().value == another_sample_user.get_id().value

    @pytest.mark.asyncio
    async def test_list_filter_by_email_contains(
        self,
        user_repo: SqlAlchemyUserRepository,
        sample_user: User,  # e.g., testuser_abc@example.com
        another_sample_user: User,  # e.g., another_testuser_xyz@example.com
        admin_user: User,  # e.g., admin_user_123@example.com
    ):
        """Tests listing users filtered by email substring (case-insensitive)."""
        # Arrange
        await user_repo.create(sample_user)
        await user_repo.create(another_sample_user)
        await user_repo.create(admin_user)
        await user_repo.session.commit()

        # Act: Search for "testuser" (should find both sample_user and another_sample_user)
        users_containing_test = await user_repo.search({"email_contains": "testuser"})
        assert len(users_containing_test) == 2
        found_ids = {user.get_id().value for user in users_containing_test}
        assert sample_user.get_id().value in found_ids
        assert another_sample_user.get_id().value in found_ids

        # Act: Search for "admin" (should find admin_user)
        users_containing_admin = await user_repo.search({"email_contains": "admin"})
        assert len(users_containing_admin) == 1
        assert users_containing_admin[0].get_id().value == admin_user.get_id().value

        # Act: Search for "example.com" (should find all)
        users_containing_domain = await user_repo.search(
            {"email_contains": "example.com"}
        )
        assert len(users_containing_domain) == 3

    @pytest.mark.asyncio
    async def test_list_filter_by_role(
        self,
        user_repo: SqlAlchemyUserRepository,
        sample_user: User,  # Roles: CUSTOMER, MANAGER
        another_sample_user: User,  # Roles: CUSTOMER
        admin_user: User,  # Roles: ADMIN
    ):
        """Tests listing users filtered by a specific role."""
        # Arrange
        await user_repo.create(sample_user)
        await user_repo.create(another_sample_user)
        await user_repo.create(admin_user)
        await user_repo.session.commit()

        # Act 1: Filter by CUSTOMER role (should find sample_user and another_sample_user)
        customer_users = await user_repo.search({"role": UserRole.CUSTOMER})
        assert len(customer_users) == 2
        customer_ids = {u.get_id().value for u in customer_users}
        assert sample_user.get_id().value in customer_ids
        assert another_sample_user.get_id().value in customer_ids

        # Act 2: Filter by MANAGER role (should find only sample_user)
        manager_users = await user_repo.search({"role": UserRole.MANAGER})
        assert len(manager_users) == 1
        assert manager_users[0].get_id().value == sample_user.get_id().value

        # Act 3: Filter by ADMIN role (should find only admin_user)
        admin_users = await user_repo.search({"role": UserRole.ADMIN})
        assert len(admin_users) == 1
        assert admin_users[0].get_id().value == admin_user.get_id().value

    @pytest.mark.asyncio
    async def test_list_pagination_limit_offset(
        self,
        user_repo: SqlAlchemyUserRepository,
        sample_user: User,
        another_sample_user: User,
        admin_user: User,
    ):
        """Tests pagination (limit and offset) for user listing."""
        # Arrange: Create users, ensuring a predictable order for pagination tests
        users_to_save = [sample_user, another_sample_user, admin_user]
        users_to_save.sort(key=lambda u: u.get_email())  # Sort User objects by email

        for user_obj in users_to_save:
            await user_repo.create(user_obj)
        await user_repo.session.commit()

        # Act 1: Limit 2, Offset 0
        users_page1 = await user_repo.search(
            {"limit": 2, "offset": 0, "sort_by": "email"}
        )
        assert len(users_page1) == 2
        assert users_page1[0].get_email() == users_to_save[0].get_email()
        assert users_page1[1].get_email() == users_to_save[1].get_email()

        # Act 2: Limit 2, Offset 1
        users_page2 = await user_repo.search(
            {"limit": 2, "offset": 1, "sort_by": "email"}
        )
        assert len(users_page2) == 2
        assert users_page2[0].get_email() == users_to_save[1].get_email()
        assert users_page2[1].get_email() == users_to_save[2].get_email()

        # Act 3: Limit 1, Offset 2
        users_page3 = await user_repo.search(
            {"limit": 1, "offset": 2, "sort_by": "email"}
        )
        assert len(users_page3) == 1
        assert users_page3[0].get_email() == users_to_save[2].get_email()

        # Act 4: Limit 1, Offset 3 (should be empty)
        users_page_empty = await user_repo.search(
            {"limit": 1, "offset": 3, "sort_by": "email"}
        )
        assert len(users_page_empty) == 0

    @pytest.mark.asyncio
    async def test_list_sort_by_email_asc_desc(
        self,
        user_repo: SqlAlchemyUserRepository,
        sample_user: User,
        another_sample_user: User,
        admin_user: User,
    ):
        """Tests sorting users by email in ascending and descending order."""
        # Arrange: Create users
        users_to_save = [sample_user, another_sample_user, admin_user]
        users_to_save.sort(key=lambda u: u.get_email())

        for user_obj in users_to_save:
            await user_repo.create(user_obj)
        await user_repo.session.commit()

        # Expected sorted emails
        expected_emails_asc = sorted([u.get_email() for u in users_to_save])
        expected_emails_desc = sorted(
            [u.get_email() for u in users_to_save], reverse=True
        )

        # Act 1: Sort ascending
        users_asc = await user_repo.search(
            {"sort_by": "email", "sort_direction": "asc"}
        )
        actual_emails_asc = [u.get_email() for u in users_asc]
        assert actual_emails_asc == expected_emails_asc

        # Act 2: Sort descending
        users_desc = await user_repo.search(
            {"sort_by": "email", "sort_direction": "desc"}
        )
        actual_emails_desc = [u.get_email() for u in users_desc]
        assert actual_emails_desc == expected_emails_desc

    @pytest.mark.asyncio
    async def test_delete_user_successfully(
        self,
        user_repo: SqlAlchemyUserRepository,
        sample_user: User,  # Use the User object directly
    ):
        """Tests deleting an existing user."""
        # Arrange: Create a user to delete
        await user_repo.create(sample_user)
        await user_repo.session.commit()

        # Act
        delete_successful = await user_repo.delete(
            sample_user.get_id()
        )  # Pass UserId object directly

        # Assert
        assert delete_successful is True

        # Verify user is no longer in the database
        retrieved_user = await user_repo.get_by_id(
            sample_user.get_id(), raise_exception=False
        )
        assert retrieved_user is None

    @pytest.mark.asyncio
    async def test_delete_user_not_found(self, user_repo: SqlAlchemyUserRepository):
        """Tests deleting a non-existent user."""
        # Act
        non_existent_id = UserId(uuid.uuid4())  # Use UserId object
        delete_successful = await user_repo.delete(non_existent_id)

        # Assert
        assert delete_successful is False
