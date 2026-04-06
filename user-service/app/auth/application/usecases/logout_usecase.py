import logging

from ..services import SessionService

logger = logging.getLogger(__name__)


class LogoutUseCase:
    def __init__(self, session: SessionService):
        self.session = session

    def execute(self, refresh_token: str, user_id: int):
        self.session.revoke_session(user_id, refresh_token)
        logger.info("logout user_id=%s", user_id)


class LogoutAllUseCase:
    def __init__(self, session: SessionService):
        self.session = session

    def execute(self, user_id: int) -> None:
        self.session.revoke_user_sessions(user_id)
        logger.info("logout all sessions user_id=%s", user_id)
