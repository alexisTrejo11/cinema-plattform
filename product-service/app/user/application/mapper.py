from app.user.domain.user import User
from .commands import UserCreateCommand, UserUpdateCommand


class UserMapper:
    @staticmethod
    def from_create_command(command: UserCreateCommand) -> User:
        return User(
            id=command.user_id,
            email=str(command.email),
            roles=command.roles,
            is_active=command.is_active,
        )

    @staticmethod
    def from_update_command(command: UserUpdateCommand, user: User) -> User:
        data = command.model_dump(exclude_unset=True)
        for k, v in data.items():
            setattr(user, k, v)

        return user
