from typing import Optional
from datetime import datetime, timezone

class SessionToken:
    def __init__(
        self,
        token_id: str,
        user_id: str,
        token: str,
        expires_at: datetime,
        is_revoked: bool = False,
        created_at: Optional[datetime] = None
    ):
        self.token_id = token_id
        self.user_id = user_id
        self.token = token
        self.expires_at = expires_at
        self.is_revoked = is_revoked
        self.created_at = created_at or datetime.now(timezone.utc)
        
    def revoke(self):
        self.is_revoked = True
    
    def is_expired(self) -> bool:
        return self.expires_at < datetime.now(timezone.utc)  
    
    def is_valid(self) -> bool:
        return not self.is_revoked and not self.is_expired()