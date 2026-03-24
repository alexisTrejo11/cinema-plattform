from app.users.application.repositories import UserRepository, User
from app.users.domain import User2FaAuthError, TwoFaAlreadyConfiguredError, InvalidTokenError
from app.token.application.service import TokenService
from app.token.domain.token import TokenType

class Enable2FAUseCase:
    def __init__(self, user_repo: UserRepository, token_service: TokenService) -> None:
        self.user_repo = user_repo
        self.token_service = token_service
    
    async def execute(self, user: User) -> tuple:
        await self._validate_user(user)

        toptp_secret_token = self.token_service.create(TokenType.TWO_FACTOR_SECRET, **user.model_dump())
        user.add_2FA_config(toptp_secret_token.code)
        qr_code = "TODO"
        
        await self.user_repo.save(user)
        
        return qr_code, toptp_secret_token.code
    
    async def _validate_user(self, user: User):
        if user.is_2fa_enabled:
            raise TwoFaAlreadyConfiguredError(message="2FA auth already configured")


class Disable2FaUseCase:
    def __init__(self, user_repo: UserRepository, token_service: TokenService) -> None:
        self.user_repo = user_repo
        self.token_service = token_service
    
    async def execute(self, user: User, token: str) -> None:
        await self._validate_user(user)

        is_valid = self.token_service.revoke(str(user.id), TokenType.VERIFICATION, token)
        if not is_valid:
            raise InvalidTokenError()
        
        user.disable_2FA_config()
        
        await self.user_repo.save(user)
        
    async def _validate_user(self, user: User):
        if not user.is_2fa_enabled:
            raise User2FaAuthError(message="User don't have 2FA enable")
