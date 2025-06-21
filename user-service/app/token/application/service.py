from typing import Any, Dict, Optional
from abc import abstractmethod, ABC
from app.token.domain.token import TokenType, Token

class TokenService(ABC):
    @abstractmethod
    def create(self, token_type: TokenType , **kwargs) -> Token:
        pass

    @abstractmethod
    def get_by_code_user_and_type(self, user_id: str, token_string: str, token_type: TokenType) -> Optional[Token]:
        pass
    
    @abstractmethod
    def revoke(self, user_id: str, token_type: TokenType, token_string: str) -> bool:
        pass

    @abstractmethod
    def revoke_all_refresh_by_user(self, user_id: str) -> None:
        pass
    
    @abstractmethod
    def verify_token(self, token_string: str, token_type: TokenType, user_id: int) -> bool:
        pass
    
    @abstractmethod
    def verify_jwt_token(self, token_string: str) -> Dict[str, Any]:
        pass
    