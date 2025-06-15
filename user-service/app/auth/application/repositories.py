from typing import Optional, List
from app.auth.domain.entities import SessionToken
from abc import abstractmethod, ABC

class SessionRepository(ABC):
    @abstractmethod
    async def create(self, token: SessionToken) -> None:
        pass
    
    @abstractmethod
    async def get_user_token(self, user_id: str, token: str) -> Optional[SessionToken]:
        pass
    
    @abstractmethod
    async def list_by_user_id(self, user_id: str) -> List[SessionToken]:
        pass
    
    @abstractmethod
    async def revoke_user_token(self, user_id: str, token: str) -> bool:
        pass
    
    @abstractmethod
    async def revoke_all_user_tokens(self, user_id: str) -> bool:
        pass
    
    @abstractmethod
    async def cleanup_expired_tokens(self) -> int:
        pass