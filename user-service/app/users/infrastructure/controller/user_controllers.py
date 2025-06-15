from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.users.application.dtos import UserResponse, UserCreate, UserUpdate
from app.users.application.use_cases import ListUserUseCase, GetUserUseCase, CreateUserUseCase, UpdateUserUseCase, DeleteUserUseCase
from .dependecies import get_user_use_case, list_user_use_case, create_user_use_case, update_user_use_case, delete_user_use_case

router = APIRouter(prefix="/api/v1/users/admin")

@router.get("/", response_model=List[UserResponse])
async def list_users(use_case: ListUserUseCase = Depends(list_user_use_case)):
    users = await use_case.execute({"size": 10 ,"number": 1})

    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, use_case: GetUserUseCase = Depends(get_user_use_case)):
    users = await use_case.execute(user_id)

    return users

@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate, use_case: CreateUserUseCase = Depends(create_user_use_case)):
    result = await use_case.execute(user_data)
    if not result.is_success():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get_error_message())
    
    return result.get_data()

@router.put("/{user_id}", response_model=UserResponse)
async def udpate_user(
    user_data: UserUpdate, 
    user_id: int,
    use_case: UpdateUserUseCase = Depends(update_user_use_case) 
):
    result = await use_case.execute(user_id, user_data)
    if not result.is_success():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get_error_message())
    
    return result.get_data()

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, use_case: DeleteUserUseCase = Depends(delete_user_use_case)):
    await use_case.execute(user_id)
