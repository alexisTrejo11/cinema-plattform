from typing import Optional, List
from app.auth.domain.entities import SessionToken
from abc import abstractmethod, ABC

class SessionTokenRepository(ABC):
    @abstractmethod
    async def create(self, refresh_token: SessionToken) -> SessionToken:
        pass
    
    @abstractmethod
    async def get_by_token(self, token: str) -> Optional[SessionToken]:
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> List[SessionToken]:
        pass
    
    @abstractmethod
    async def revoke_token(self, token: str) -> bool:
        pass
    
    @abstractmethod
    async def revoke_all_user_tokens(self, user_id: str) -> bool:
        pass
    
    @abstractmethod
    async def cleanup_expired_tokens(self) -> int:
        pass