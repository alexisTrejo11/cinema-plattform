from typing import Optional, List
from app.auth.domain.entities import JWTToken, TokenType
from abc import abstractmethod, ABC

class SessionRepository(ABC):
    @abstractmethod
    def create(self, token: JWTToken) -> None:
        pass
    
    @abstractmethod
    def get_user_token(self, user_id: str, token_code: str, token_type: TokenType) -> Optional[JWTToken]:
        pass
    
    @abstractmethod
    def list_by_user_id(self, user_id: str) -> List[JWTToken]:
        pass
    
    @abstractmethod
    def revoke_user_token(self, user_id: str, token_code: str, token_type: TokenType) -> bool:
        pass
    
    @abstractmethod
    def revoke_all_user_tokens(self, user_id: str) -> bool:
        pass
    
    @abstractmethod
    def cleanup_expired_tokens(self) -> int:
        pass