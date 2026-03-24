from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.shared.pagination import PaginationParams as PageParams
from app.auth.infrastructure.api.dependencies import get_logged_admin_user
from app.users.application.dtos import UserResponse, UserCreate, UserUpdate
from app.users.domain import User
from .dependencies import UsersUseCasesContainer, get_user_use_cases

router = APIRouter(prefix="/api/v1/users/admin", tags=["User Administration"])


@router.get(
    "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve a list of all users",
    description="Fetches a paginated list of all registered users. Requires 'admin' role.",
)
async def list_users(
    use_cases: UsersUseCasesContainer = Depends(get_user_use_cases),
    _admin_user: User = Depends(get_logged_admin_user),
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    """
    Retrieves a list of all users.
    """
    page = PageParams(offset, limit)
    users = await use_cases.list_users.execute(page)
    return [UserResponse.from_domain(user) for user in users]


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a single user by ID",
    description="Fetches detailed information for a specific user using their unique ID. Requires 'admin' role.",
)
async def get_user(
    user_id: int,
    use_cases: UsersUseCasesContainer = Depends(get_user_use_cases),
    _admin_user: User = Depends(get_logged_admin_user),
):
    """
    Retrieves a single user by their ID.
    """
    user = await use_cases.get_user.execute(user_id)
    return UserResponse.from_domain(user)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Registers a new user in the system. Requires 'admin' role.",
)
async def create_user(
    user_data: UserCreate,
    use_cases: UsersUseCasesContainer = Depends(get_user_use_cases),
    _admin_user: User = Depends(get_logged_admin_user),
):
    """
    Creates a new user.
    """
    result = await use_cases.create_user.execute(user_data)
    if not result.is_success():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get_error_message(),
        )

    user = result.get_data()
    return UserResponse.from_domain(user)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing user",
    description="Updates the details of an existing user identified by their ID. Requires 'admin' role.",
)
async def udpate_user(
    user_data: UserUpdate,
    user_id: int,
    use_cases: UsersUseCasesContainer = Depends(get_user_use_cases),
    _admin_user: User = Depends(get_logged_admin_user),
):
    """
    Updates an existing user by their ID.
    """
    result = await use_cases.update_user.execute(user_id, user_data)
    if not result.is_success():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get_error_message(),
        )

    user = result.get_data()
    return UserResponse.from_domain(user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, str],
    summary="Delete a user by ID",
    description="Deletes a user from the system using their unique ID. Requires 'admin' role.",
)
async def delete_user(
    user_id: int,
    use_cases: UsersUseCasesContainer = Depends(get_user_use_cases),
    _admin_user: User = Depends(get_logged_admin_user),
):
    """
    Deletes a user by their ID.
    """
    await use_cases.delete_user.execute(user_id)
    return {"message": f"User with ID {user_id} deleted successfully."}


@router.patch(
    "/{user_id}/activate",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, str],
)
async def activate_user(
    user_id: int,
    activation_token: str = Query(..., min_length=1),
    use_cases: UsersUseCasesContainer = Depends(get_user_use_cases),
    _admin_user: User = Depends(get_logged_admin_user),
):
    """
    Activates a user by their ID.
    """
    await use_cases.activate_user.execute(user_id, activation_token)
    return {"message": f"User with ID {user_id} activated successfully."}


@router.patch(
    "/{user_id}/ban",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, str],
)
async def ban_user(
    user_id: int,
    use_cases: UsersUseCasesContainer = Depends(get_user_use_cases),
    _admin_user: User = Depends(get_logged_admin_user),
):
    """
    Bans a user by their ID.
    """
    await use_cases.ban_user.execute(user_id)
    return {"message": f"User with ID {user_id} banned successfully."}
