from dataclasses import dataclass

from app.auth.application.services import (
    AuthValidationService,
    PasswordService,
    TokenProvider,
)
from app.users.domain import UserRepository

from .use_cases import (
    ActivateUser,
    BanUserUseCase,
    CreateUserUseCase,
    DeleteUserUseCase,
    GetUserUseCase,
    ListUsersUseCase,
    UpdateUserUseCase,
)


@dataclass
class UsersUseCasesContainer:
    list_users: ListUsersUseCase
    get_user: GetUserUseCase
    create_user: CreateUserUseCase
    update_user: UpdateUserUseCase
    delete_user: DeleteUserUseCase
    activate_user: ActivateUser
    ban_user: BanUserUseCase


def build_users_use_cases(
    repository: UserRepository,
    password_service: PasswordService,
    validation_service: AuthValidationService,
    token_service: TokenProvider,
) -> UsersUseCasesContainer:
    return UsersUseCasesContainer(
        list_users=ListUsersUseCase(repository),
        get_user=GetUserUseCase(repository),
        create_user=CreateUserUseCase(repository, password_service, validation_service),
        update_user=UpdateUserUseCase(repository, validation_service, password_service),
        delete_user=DeleteUserUseCase(repository),
        activate_user=ActivateUser(repository, token_service),
        ban_user=BanUserUseCase(repository),
    )
