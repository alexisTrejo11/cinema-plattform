from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from app.shared.response import ApiResponse, ErrorResponse
from app.shared.pagintation import PaginationParams as PageParams
from app.auth.infrastructure.api.dependencies import get_logged_admin_user
from app.users.application.dtos import UserResponse, UserCreate, UserUpdate
from app.users.domain.entities import  User
from app.users.application.use_cases import ListUsersUseCase, GetUserUseCase, CreateUserUseCase, UpdateUserUseCase, DeleteUserUseCase, BanUserUseCase
from .dependecies import get_user_use_case, list_user_use_case, create_user_use_case, update_user_use_case, delete_user_use_case, ban_user_use_case
import logging

logger = logging.getLogger("app")
router = APIRouter(prefix="/api/v1/users/admin", tags=["User Administration"])

common_error_responses = {
    400: {"model": ApiResponse[ErrorResponse], "description": "Bad Request - Invalid input or business rule violation."},
    401: {"model": ApiResponse[ErrorResponse], "description": "Unauthorized - Authentication required or failed."},
    403: {"model": ApiResponse[ErrorResponse], "description": "Forbidden - User does not have the necessary permissions."},
    404: {"model": ApiResponse[ErrorResponse], "description": "Not Found - The requested resource was not found."},
    500: {"model": ApiResponse[ErrorResponse], "description": "Internal Server Error - An unexpected server error occurred."}
}

@router.get(
    "/",
    response_model=ApiResponse[List[UserResponse]],
    status_code=status.HTTP_200_OK,
    summary="Retrieve a list of all users",
    description="Fetches a paginated list of all registered users. Requires 'admin' role.",
    responses={
        200: {"model": ApiResponse[List[UserResponse]], "description": "Successfully retrieved list of users."},
        **common_error_responses
    }
)
async def list_users(
    request: Request,
    use_case: ListUsersUseCase = Depends(list_user_use_case),
    admin_user: User = Depends(get_logged_admin_user),
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10
    ):
    """
    Retrieves a list of all users.
    """
    logger.info(f"LIST users started | admin:{admin_user.id} | client:{request.client.host if request.client else None}")
    
    try:
        page = PageParams(offset, limit)
        users = await use_case.execute(page)
        logger.info(f"LIST users success | count:{len(users)}")
        
        response = ApiResponse.success(users, "User List Retrieved")
        return response
    except Exception as e:
        logger.error(f"LIST users failed | error:{str(e)}")
        raise
    
    
@router.get(
    "/{user_id}",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve a single user by ID",
    description="Fetches detailed information for a specific user using their unique ID. Requires 'admin' role.",
    responses={
        200: {"model": ApiResponse[UserResponse], "description": "Successfully retrieved user details."},
        404: {"model": ApiResponse[ErrorResponse], "description": "User Not Found - The user with the specified ID does not exist."},
        **common_error_responses
    }
)
async def get_user(
    request: Request,
    user_id: int, 
    use_case: GetUserUseCase = Depends(get_user_use_case),
    admin_user: User = Depends(get_logged_admin_user)
):
    """
    Retrieves a single user by their ID.
    """
    logger.info(f"GET user started | user_id:{user_id} | admin:{admin_user.id} | client:{request.client.host if request.client else None}")
    
    try:
        user = await use_case.execute(user_id)
        logger.info(f"GET user success | user_id:{user_id}")
        
        response = ApiResponse.success(user, f"User with ID {user_id} retrieved successfully.")
        return response    
    except Exception as e:
        logger.error(f"GET user failed | user_id:{user_id} | error:{str(e)}")
        raise
    

@router.post(
    "/",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Registers a new user in the system. Requires 'admin' role.",
    responses={
        201: {"model": ApiResponse[UserResponse], "description": "User successfully created."},
        400: {"model": ApiResponse[ErrorResponse], "description": "Bad Request - Invalid user data."},
        409: {"model": ApiResponse[ErrorResponse], "description": "Conflict - User provided unique fields that already exists (e.g., email)."},
        **common_error_responses
    }
)
async def create_user(
    request: Request,
    user_data: UserCreate, 
    use_case: CreateUserUseCase = Depends(create_user_use_case),
    admin_user: User = Depends(get_logged_admin_user)
    
):
    """
    Creates a new user.
    """
    logger.info(f"POST user started | email:{user_data.email} | admin:{admin_user.id} | client {request.client.host if request.client else None} ")
    
    try:
        result = await use_case.execute(user_data)
        if not result.is_success():
            logger.warning(f"POST user failed | email:{user_data.email} | reason:{result.get_error_message()}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get_error_message())
        
        user = result.get_data()
        logger.info(f"POST user success | user_id:{user.id} | email:{user_data.email}")
        
        response = ApiResponse.success(user, "User created successfully.")
        return response
    except Exception as e:
        logger.error(f"POST user failed | email:{user_data.email} | error:{str(e)}")
        raise
    
    
@router.put(
    "/{user_id}",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Update an existing user",
    description="Updates the details of an existing user identified by their ID. Requires 'admin' role.",
    responses={
        200: {"model": ApiResponse[UserResponse], "description": "User successfully updated."},
        400: {"model": ApiResponse[ErrorResponse], "description": "Bad Request - Invalid update data."},
        404: {"model": ApiResponse[ErrorResponse], "description": "User Not Found - The user with the specified ID does not exist."},
        **common_error_responses
    }
)
async def udpate_user(
    request: Request,
    user_data: UserUpdate, 
    user_id: int,
    use_case: UpdateUserUseCase = Depends(update_user_use_case) ,
    admin_user: User = Depends(get_logged_admin_user)
):
    """
    Updates an existing user by their ID.
    """
    logger.info(f"PUT user started | user_id:{user_id} | admin:{admin_user.id} |  client:{request.client.host if request.client else None}")
    
    try:
        result = await use_case.execute(user_id, user_data)
        
        if not result.is_success():
            logger.warning(f"PUT user failed | user_id:{user_id} | reason:{result.get_error_message()}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get_error_message())
        
        user = result.get_data()
        logger.info(f"PUT user success | user_id:{user_id}")
        
        response = ApiResponse.success(user, f"User with ID {user_id} updated successfully.")
        return response
    except Exception as e:
        logger.error(f"PUT user failed | user_id:{user_id} | error:{str(e)}")
        raise
    
    
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[None],
    summary="Delete a user by ID",
    description="Deletes a user from the system using their unique ID. Requires 'admin' role.",
    responses={
        200: {"model": ApiResponse[None], "description": "User successfully deleted."},
        404: {"model": ApiResponse[ErrorResponse], "description": "User Not Found - The user with the specified ID does not exist."},
        **common_error_responses
    }
)
async def delete_user(
    request: Request,
    user_id: int, 
    use_case: DeleteUserUseCase = Depends(delete_user_use_case),
    admin_user: User = Depends(get_logged_admin_user)
):
    """
    Deletes a user by their ID.
    """
    logger.info(f"DELETE user started | user_id:{user_id} | admin:{admin_user.id} | client:{request.client.host if request.client else None}")
    try:
        await use_case.execute(user_id)
        logger.info(f"DELETE user success | user_id:{user_id}")
        
        return ApiResponse.success(None, f"User with ID {user_id} deleted successfully.")
    except Exception as e:
        logger.error(f"DELETE user failed | user_id:{user_id} | error:{str(e)}")
        raise


@router.patch(
    "{user_id}/activate", 
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[None],
)

    
@router.patch(
    "{user_id}/ban", 
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[None],
)
async def ban_user(
    request: Request,
    user_id: int, 
    use_case: BanUserUseCase = Depends(ban_user_use_case),
    
    admin_user: User = Depends(get_logged_admin_user)
):
    """
    Bans a user by their ID.
    """
    logger.info(f"PATCH user ban started | user_id:{user_id} | admin:{admin_user.id} | client:{request.client.host if request.client else None}")

    await use_case.execute(user_id)

    logger.info(f"PATCH user banned | user_id:{user_id}")
    
    return ApiResponse.success(None, f"User with ID {user_id} banned successfully.")
