from typing import Any
from app.token.application.service import TokenService
from app.token.domain.token import TokenType
from ..services import SessionService

class LogoutUseCase:
    def __init__(self, session: SessionService):
        self.session = session
    
    def execute(self, refresh_token: str, user_id: int) :
        return self.session.revoke_session(user_id, refresh_token)


class LogoutAllUseCase:
    def __init__(self, session: SessionService):
        self.session = session
    
    def execute(self, user_id: int) -> None:
        return self.session.revoke_user_sessions(user_id)
