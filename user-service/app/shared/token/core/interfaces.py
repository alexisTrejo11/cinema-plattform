from abc import abstractmethod, ABC
from typing import Any, Dict, Optional, List
from .token import TokenType, Token


class TokenProvider(ABC):
    @abstractmethod
    def create(self, token_type: TokenType, **kwargs) -> Token:
        pass

    @abstractmethod
    def get_by_code_user_and_type(
        self, user_id: str, token_string: str, token_type: TokenType
    ) -> Optional[Token]:
        pass

    @abstractmethod
    def revoke(self, user_id: str, token_type: TokenType, token_string: str) -> bool:
        pass

    @abstractmethod
    def revoke_all_refresh_by_user(self, user_id: str) -> None:
        pass

    @abstractmethod
    def verify_token(
        self, token_string: str, token_type: TokenType, user_id: int
    ) -> bool:
        pass

    @abstractmethod
    def verify_jwt_token(self, token_string: str) -> Dict[str, Any]:
        pass


class TokenRepository(ABC):
    @abstractmethod
    def create(self, token: Token) -> None:
        pass

    @abstractmethod
    def get_user_token(
        self, user_id: str, token_code: str, token_type: TokenType
    ) -> Optional[Token]:
        pass

    @abstractmethod
    def list_by_user_id(self, user_id: str) -> List[Token]:
        pass

    @abstractmethod
    def revoke_user_token(
        self, user_id: str, token_code: str, token_type: TokenType
    ) -> bool:
        pass

    @abstractmethod
    def revoke_all_user_tokens(self, user_id: str) -> bool:
        pass

    @abstractmethod
    def cleanup_expired_tokens(self) -> int:
        pass
