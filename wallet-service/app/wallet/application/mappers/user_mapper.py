
from app.domain.models import User
from app.application.dtos.user_dtos import UserDTO, CreateUserDTO

def user_to_dto(user: User) -> UserDTO:
    """Maps a User domain object to a UserDTO."""
    return UserDTO.from_orm(user)

def create_user_dto_to_domain(dto: CreateUserDTO) -> User:
    """Maps a CreateUserDTO to a User domain object."""
    return User(username=dto.username, email=dto.email)

