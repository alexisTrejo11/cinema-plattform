from typing import Any
from app.users.domain.entities import User
from app.token.application.service import TokenService
from app.shared.response import Result
from app.token.domain.token import TokenType
from app.notification.application.services import NotificationService
from app.notification.domain.entitites import Notification, NotificationType
from ..services import SessionService, AuthValidationService
from ..dtos import LoginRequest, RefreshTokenRequest, SessionResponse
from app.shared.qr import generate_QR
import pyotp


class LoginUseCase:
    def __init__(
        self, 
        session_service: SessionService, 
        validation_service: AuthValidationService, 
        token_service: TokenService,
    ):
        self.session_service = session_service
        self.token_service = token_service
        self.validation_service = validation_service
    
    
    async def execute(self, request: LoginRequest) -> Result[Any]:
        user = await self.validation_service.authenticate_user(request.identifier_field, request.password)
        if not user:
            return Result.error("User not found with given credentials")
        
        self.validation_service.validate_account_status_for_login(user)
        session = await self.session_service.create_session(user)
        
        return Result.success(session)
    

class TwoFALoginUseCase:
    def __init__(
        self, 
        token_service: TokenService, 
        notification_service: NotificationService, 
        validation_service: AuthValidationService,
        session_service: SessionService, 

    ) -> None:
        self.session_service = session_service
        self.token_service = token_service
        self.notification_service = notification_service
        self.validation_service = validation_service

    async def execute(self, request: LoginRequest) -> Result:
        user = await self.validation_service.authenticate_user(request.identifier_field, request.password)
        if not user:
            return Result.error("User not found with given credentials")
        
        if not request.twoFACode:
            return await self._send_qr(request, user)
    
        return await self._verify_qr(request, user)

    async def _send_qr(self, request: LoginRequest, user:User):
        if not user.totp_secret:
            raise ValueError("User dont have 2FA secret")
                
        token = self.token_service.create(TokenType.TWO_FA, **{"email": user.email, "totp_secret": user.totp_secret})
        
        qr = generate_QR(token.code)
        return Result.success(qr)
    
    async def _verify_qr(self, request: LoginRequest, user: User):
        assert self.validation_service.validate_2FA_Access(user.id, request.twoFACode) 
        session = await self.session_service.create_session(user)
        
        return Result.success(session)


class RefreshTokenUseCase:
    def __init__(self, session_service: SessionService):
        self.session_service = session_service
    
    async def execute(self, request: RefreshTokenRequest, user: User) -> SessionResponse:
        token_response = await self.session_service.refresh_session(request, user)
        return token_response
