from dataclasses import dataclass

from app.shared.notification.domain.services import NotificationService
from app.shared.token.core import TokenProvider
from app.users.domain import UserRepository

from ..services import AuthValidationService, PasswordService, SessionService
from .login_usecase import LoginUseCase, RefreshTokenUseCase, TwoFALoginUseCase
from .logout_usecase import LogoutAllUseCase, LogoutUseCase
from .signup_usecase import SignUpUseCase
from .two_fa_usecases import Disable2FaUseCase, Enable2FAUseCase


@dataclass
class AuthUseCasesContainer:
    signup: SignUpUseCase
    login: LoginUseCase
    logout: LogoutUseCase
    logout_all: LogoutAllUseCase
    refresh_token: RefreshTokenUseCase
    enable_2fa: Enable2FAUseCase
    disable_2fa: Disable2FaUseCase
    two_fa_login: TwoFALoginUseCase


def build_auth_use_cases(
    user_repo: UserRepository,
    password_service: PasswordService,
    validation_service: AuthValidationService,
    token_service: TokenProvider,
    session_service: SessionService,
    notification_service: NotificationService,
) -> AuthUseCasesContainer:
    return AuthUseCasesContainer(
        signup=SignUpUseCase(
            user_repository=user_repo,
            validation_service=validation_service,
            password_service=password_service,
            token_service=token_service,
            notification_service=notification_service,
        ),
        login=LoginUseCase(session_service, validation_service, token_service),
        logout=LogoutUseCase(session_service),
        logout_all=LogoutAllUseCase(session_service),
        refresh_token=RefreshTokenUseCase(session_service),
        enable_2fa=Enable2FAUseCase(user_repo, token_service),
        disable_2fa=Disable2FaUseCase(user_repo, token_service),
        two_fa_login=TwoFALoginUseCase(
            token_service,
            validation_service,
            session_service,
        ),
    )
