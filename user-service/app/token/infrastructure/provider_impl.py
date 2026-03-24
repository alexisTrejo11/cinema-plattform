import logging
from datetime import datetime
from typing import Any, Dict, Optional

from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from app.auth.domain.exceptions import InvalidCredentialsException
from app.token.domain.interfaces import TokenRepository, TokenProvider
from app.token.domain.token import Token, TokenType
from config.security import decode_jwt_token

from .factory import TokenFactory

logger = logging.getLogger("app")


class TokenProviderImpl(TokenProvider):
    def __init__(
        self, token_repository: TokenRepository, secret_key: str, algorithm: str
    ) -> None:
        self.token_repository = token_repository
        self.secret_key = secret_key
        self.algorithm = algorithm
        super().__init__()

    def create(self, token_type: TokenType, **kwargs) -> Token:
        token = TokenFactory().create(token_type, **kwargs)

        self.token_repository.create(token)
        return token

    def verify_token(
        self, token_string: str, token_type: TokenType, user_id: int
    ) -> bool:
        if token_type in (TokenType.JWT_ACCESS, TokenType.JWT_REFRESH):
            try:
                self.verify_jwt_token(token_string)
                return True
            except InvalidCredentialsException:
                return False

        token = self.token_repository.get_user_token(
            str(user_id), token_string, token_type
        )
        if not token:
            return False
        if token.is_revoked:
            return False
        if token.expires_at <= datetime.now():
            return False
        return True

    def verify_jwt_token(self, token_string: str) -> Dict[str, Any]:
        try:
            return decode_jwt_token(token_string)
        except ExpiredSignatureError as e:
            logger.error("(verify_jwt_token): Token expired: %s", e)
            raise InvalidCredentialsException("Token has expired") from e
        except InvalidTokenError as e:
            logger.error("(verify_jwt_token): Invalid JWT: %s", e)
            raise InvalidCredentialsException(f"Invalid token: {e}") from e
        except Exception as e:
            logger.error(
                "(verify_jwt_token): Unexpected error: %s: %s",
                type(e).__name__,
                e,
            )
            raise InvalidCredentialsException(
                f"Token verification failed unexpectedly: {e}"
            ) from e

    def get_by_code_user_and_type(
        self, user_id: str, token_string: str, token_type: TokenType
    ) -> Optional[Token]:
        token = self.token_repository.get_user_token(user_id, token_string, token_type)
        if token and not token.is_revoked:
            return token

        return None

    def revoke(self, user_id: str, token_type: TokenType, token_string: str) -> bool:
        token = self.token_repository.get_user_token(user_id, token_string, token_type)
        if not token or token.is_revoked:
            return False

        self.token_repository.revoke_user_token(user_id, token_string, token_type)
        return True

    def revoke_all_refresh_by_user(self, user_id: str) -> None:
        self.token_repository.revoke_all_user_tokens(user_id)
