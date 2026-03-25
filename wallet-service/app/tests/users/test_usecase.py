import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from typing import Dict, Any, List
from datetime import datetime, timezone
import uuid

from app.user.domain.user import User, UserRole
from app.user.domain.value_objects import UserId
from app.user.domain.exceptions import UserNotFoundException
from app.user.domain.repository import UserRepository
from app.user.application.dtos import (
    UserCreateCommand,
    UserResponse,
)
from app.user.application.usecases import (
    GetUserByIdUseCase,
    GetUserByEmailUseCase,
    ListUsersUseCase,
    CreateUserUseCase,
    UpdateUserUseCase,
    SoftDeleteUserUseCase,
)


# --- Fixtures for Mocking and Test Data ---
@pytest.fixture
def mock_user_repository() -> AsyncMock:
    """Provides an AsyncMock for the UserRepository."""
    return AsyncMock(spec=UserRepository)


@pytest.fixture
def sample_user_data_for_domain() -> Dict[str, Any]:
    """Provides a dictionary representing raw data for a domain User."""
    return {
        "id": UserId(uuid.uuid4()),
        "email": "test@example.com",
        "roles": [UserRole.CUSTOMER],
        "is_active": True,
        "created_at": datetime.now(timezone.utc).replace(tzinfo=None),
        "updated_at": datetime.now(timezone.utc).replace(tzinfo=None),
    }


@pytest.fixture
def sample_domain_user(sample_user_data_for_domain: Dict[str, Any]) -> User:
    """Provides a sample User domain entity with a to_dict method."""
    # We need to ensure the mock User object has a .to_dict() method
    user = MagicMock(spec=User)
    
    # Create a mock UserId object with to_string method
    mock_user_id = MagicMock(spec=UserId)
    mock_user_id.value = sample_user_data_for_domain["id"].value
    mock_user_id.to_string.return_value = str(sample_user_data_for_domain["id"].value)
    
    user.get_id.return_value = mock_user_id
    user.get_email.return_value = sample_user_data_for_domain["email"]
    user.get_roles.return_value = sample_user_data_for_domain["roles"]
    user.is_active.return_value = sample_user_data_for_domain["is_active"]
    user.get_created_at.return_value = sample_user_data_for_domain["created_at"]
    user.get_updated_at.return_value = sample_user_data_for_domain["updated_at"]
    user.to_dict.return_value = {
        "id": sample_user_data_for_domain["id"].value,  # Return UUID directly
        "email": sample_user_data_for_domain["email"],
        "roles": [
            role.value for role in sample_user_data_for_domain["roles"]
        ],  # Return enum values
        "is_active": sample_user_data_for_domain["is_active"],
        "created_at": sample_user_data_for_domain["created_at"],  # Return datetime directly
        "updated_at": sample_user_data_for_domain["updated_at"],  # Return datetime directly
    }
    return user


@pytest.fixture
def another_domain_user(sample_domain_user: User) -> User:
    """Provides another sample User domain entity."""
    user = MagicMock(spec=User)
    new_id = UserId(uuid.uuid4())
    new_email = f"another_{uuid.uuid4().hex[:8]}@example.com"
    
    # Create a mock UserId object with to_string method
    mock_user_id = MagicMock(spec=UserId)
    mock_user_id.value = new_id.value
    mock_user_id.to_string.return_value = str(new_id.value)
    
    user.get_id.return_value = mock_user_id
    user.get_email.return_value = new_email
    user.get_roles.return_value = [UserRole.MANAGER]
    user.is_active.return_value = False
    user.get_created_at.return_value = datetime.now(timezone.utc).replace(tzinfo=None)
    user.get_updated_at.return_value = datetime.now(timezone.utc).replace(tzinfo=None)
    user.to_dict.return_value = {
        "id": new_id.value,  # Return UUID directly
        "email": new_email,
        "roles": [UserRole.MANAGER.value],
        "is_active": False,
        "created_at": datetime.now(timezone.utc).replace(tzinfo=None),  # Return datetime directly
        "updated_at": datetime.now(timezone.utc).replace(tzinfo=None),  # Return datetime directly
    }
    return user


@pytest.fixture
def user_create_command() -> UserCreateCommand:
    """Provides a sample UserCreateCommand DTO."""
    return UserCreateCommand(
        email=f"newuser_{uuid.uuid4().hex[:8]}@example.com",
        roles=[UserRole.CUSTOMER],
        is_active=True,
    )


@pytest.fixture
def user_update_command() -> UserCreateCommand:
    """Provides a sample UserCreateCommand DTO for updates."""
    return UserCreateCommand(
        email=f"updateduser_{uuid.uuid4().hex[:8]}@example.com",
        roles=[UserRole.ADMIN],
        is_active=False,
    )


# --- Test Cases for GetUserByIdUseCase ---


@pytest.mark.asyncio
async def test_get_user_by_id_success(
    mock_user_repository: AsyncMock, sample_domain_user: User
):
    """Tests that GetUserByIdUseCase retrieves a user successfully."""
    mock_user_repository.get_by_id.return_value = sample_domain_user

    use_case = GetUserByIdUseCase(user_repository=mock_user_repository)
    user_id = sample_domain_user.get_id()
    result = await use_case.execute(user_id)

    mock_user_repository.get_by_id.assert_called_once_with(user_id.to_string())
    assert isinstance(result, UserResponse)
    assert result.id == user_id.value
    assert result.email == sample_domain_user.get_email()
    assert result.roles == [role.value for role in sample_domain_user.get_roles()]


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(mock_user_repository: AsyncMock):
    """Tests that GetUserByIdUseCase raises UserNotFoundException when user is not found."""
    mock_user_repository.get_by_id.return_value = None

    use_case = GetUserByIdUseCase(user_repository=mock_user_repository)
    non_existent_id = UserId(uuid.uuid4())

    with pytest.raises(UserNotFoundException) as exc_info:
        await use_case.execute(non_existent_id)

    mock_user_repository.get_by_id.assert_called_once_with(non_existent_id.to_string())
    assert str(non_existent_id.value) in str(exc_info.value)


# --- Test Cases for GetUserByEmailUseCase ---


@pytest.mark.asyncio
async def test_get_user_by_email_success(
    mock_user_repository: AsyncMock, sample_domain_user: User
):
    """Tests that GetUserByEmailUseCase retrieves a user successfully by email."""
    mock_user_repository.get_by_email.return_value = sample_domain_user

    use_case = GetUserByEmailUseCase(user_repository=mock_user_repository)
    user_email = sample_domain_user.get_email()
    result = await use_case.execute(user_email)

    mock_user_repository.get_by_email.assert_called_once_with(user_email)
    assert isinstance(result, UserResponse)
    assert result.email == user_email
    assert result.id == sample_domain_user.get_id().value


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(mock_user_repository: AsyncMock):
    """Tests that GetUserByEmailUseCase raises UserNotFoundException when user is not found."""
    mock_user_repository.get_by_email.return_value = None

    use_case = GetUserByEmailUseCase(user_repository=mock_user_repository)
    non_existent_email = "nonexistent@example.com"

    with pytest.raises(UserNotFoundException) as exc_info:
        await use_case.execute(non_existent_email)

    mock_user_repository.get_by_email.assert_called_once_with(non_existent_email)
    assert non_existent_email in str(exc_info.value)


# --- Test Cases for ListUsersUseCase ---


@pytest.mark.asyncio
async def test_list_users_no_params(
    mock_user_repository: AsyncMock, sample_domain_user: User, another_domain_user: User
):
    """Tests listing all users without any filtering parameters."""
    mock_user_repository.list.return_value = [sample_domain_user, another_domain_user]

    use_case = ListUsersUseCase(user_repository=mock_user_repository)
    params = {}
    result = await use_case.execute(params)

    mock_user_repository.list.assert_called_once_with(params)
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, UserResponse) for item in result)
    assert {u.id for u in result} == {
        sample_domain_user.get_id().value,
        another_domain_user.get_id().value,
    }


@pytest.mark.asyncio
async def test_list_users_with_params(
    mock_user_repository: AsyncMock, sample_domain_user: User
):
    """Tests listing users with filtering parameters."""
    mock_user_repository.list.return_value = [sample_domain_user]

    use_case = ListUsersUseCase(user_repository=mock_user_repository)
    params = {"is_active": True, "email_contains": "test"}
    result = await use_case.execute(params)

    mock_user_repository.list.assert_called_once_with(params)
    assert len(result) == 1
    assert result[0].id == sample_domain_user.get_id().value


@pytest.mark.asyncio
async def test_list_users_empty_list(mock_user_repository: AsyncMock):
    """Tests listing users when no users are found."""
    mock_user_repository.list.return_value = []

    use_case = ListUsersUseCase(user_repository=mock_user_repository)
    params = {"is_active": False}
    result = await use_case.execute(params)

    mock_user_repository.list.assert_called_once_with(params)
    assert isinstance(result, list)
    assert len(result) == 0


# --- Test Cases for CreateUserUseCase ---


@pytest.mark.asyncio
async def test_create_user_success(
    mock_user_repository: AsyncMock,
    user_create_command: UserCreateCommand,
):
    """Tests that CreateUserUseCase successfully creates a user."""
    # Create a mock user that matches the command data
    created_user = MagicMock(spec=User)
    created_user.to_dict.return_value = {
        "id": uuid.uuid4(),
        "email": user_create_command.email,
        "roles": user_create_command.roles,  # roles are already strings due to use_enum_values = True
        "is_active": user_create_command.is_active,
        "created_at": datetime.now(timezone.utc).replace(tzinfo=None),
        "updated_at": datetime.now(timezone.utc).replace(tzinfo=None),
    }
    
    mock_user_repository.save.return_value = created_user

    use_case = CreateUserUseCase(user_repository=mock_user_repository)
    result = await use_case.execute(user_create_command)

    # Assert that the repository's save method was called with the correct data
    # Use command.model_dump(exclude_unset=True) if your save method handles partial updates
    # Here, for creation, it's usually the full data.
    mock_user_repository.save.assert_called_once_with(
        **user_create_command.model_dump()
    )

    assert isinstance(result, UserResponse)
    assert result.email == user_create_command.email
    assert result.is_active == user_create_command.is_active
    assert result.roles == user_create_command.roles


@pytest.mark.asyncio
async def test_update_user_not_found(
    mock_user_repository: AsyncMock, user_update_command: UserCreateCommand
):
    """Tests that UpdateUserUseCase raises UserNotFoundException when user to update is not found."""
    mock_user_repository.get_by_id.return_value = None  # User not found

    use_case = UpdateUserUseCase(user_repository=mock_user_repository)
    non_existent_id = UserId(uuid.uuid4())

    with pytest.raises(UserNotFoundException) as exc_info:
        await use_case.execute(non_existent_id, user_update_command)

    mock_user_repository.get_by_id.assert_called_once_with(non_existent_id.to_string())
    mock_user_repository.save.assert_not_called()  # Save should not be called if user not found
    assert str(non_existent_id.value) in str(exc_info.value)


# --- Test Cases for SoftDeleteUserUseCase ---
@pytest.mark.asyncio
async def test_soft_delete_user_success(
    mock_user_repository: AsyncMock, sample_domain_user: User
):
    """Tests that SoftDeleteUserUseCase successfully soft deletes a user."""
    mock_user_repository.get_by_id.return_value = sample_domain_user  # User exists
    mock_user_repository.delete.return_value = True  # Deletion is successful

    use_case = SoftDeleteUserUseCase(user_repository=mock_user_repository)
    user_id = sample_domain_user.get_id()
    await use_case.execute(user_id)

    mock_user_repository.get_by_id.assert_called_once_with(user_id.to_string())
    mock_user_repository.delete.assert_called_once_with(user_id.to_string())


@pytest.mark.asyncio
async def test_soft_delete_user_not_found(mock_user_repository: AsyncMock):
    """Tests that SoftDeleteUserUseCase raises UserNotFoundException when user to delete is not found."""
    mock_user_repository.get_by_id.return_value = None  # User not found

    use_case = SoftDeleteUserUseCase(user_repository=mock_user_repository)
    non_existent_id = UserId(uuid.uuid4())

    with pytest.raises(UserNotFoundException) as exc_info:
        await use_case.execute(non_existent_id)

    mock_user_repository.get_by_id.assert_called_once_with(non_existent_id.to_string())
    mock_user_repository.delete.assert_not_called()  # Delete should not be called if user not found
    assert str(non_existent_id.value) in str(exc_info.value)
