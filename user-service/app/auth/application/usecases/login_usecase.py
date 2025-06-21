from typing import Any
from app.users.domain.entities import User
from app.token.application.service import TokenService
from app.shared.response import Result
from app.token.domain.token import TokenType
from app.notification.application.services import NotificationService
from app.notification.domain.entitites import Notification, NotificationType
from ..services import SessionService, AuthValidationService
from ..dtos import LoginRequest, RefreshTokenRequest, SessionResponse

class LoginUseCase:
    def __init__(
        self, 
        session_service: SessionService, 
        validation_service: AuthValidationService, 
        token_service: TokenService,
        notification_service: NotificationService
    ):
        self.session_service = session_service
        self.token_service = token_service
        self.validation_service = validation_service
        self.notification_service = notification_service
    
    
    async def execute(self, request: LoginRequest) -> Result[Any]:
        user = await self.validation_service.authenticate_user(request.identifier_field, request.password)
        if not user:
            return Result.error("User not found with given credentials")
        
        self.validation_service.validate_account_status_for_login(user)
                
        if user.is_2fa_enabled:
            return await self._proccess_2fa_login(user, request)
        else:
            return await self.proccess_login(user)
      
            
    async def proccess_login(self, user) -> Result:
        session = await self.session_service.create_session(user)
        return Result.success(session)
    
    
    async def _proccess_2fa_login(self, user: User, request: LoginRequest) -> Result:
        if not request.twoFACode:
            token = self.token_service.create(TokenType.VERIFICATION, **{"user_id" : user.id})
            
            notification = Notification(user=user, token=token.code, notification_type=NotificationType.EMAIL)
            await self.notification_service.send_notification(notification)
            
            return Result.success()
        else:
            self.validation_service.validate_2FA_Access(user.id, request.twoFACode) 
            
            self.token_service.revoke(str(user.id), TokenType.VERIFICATION, request.twoFACode)
            session = await self.session_service.create_session(user)
            
            return Result.success(session)
    


class RefreshTokenUseCase:
    def __init__(self, session_service: SessionService):
        self.session_service = session_service
    
    async def execute(self, request: RefreshTokenRequest, user: User) -> SessionResponse:
        token_response = await self.session_service.refresh_session(request, user)
        return token_response
