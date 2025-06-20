from enum import Enum
from datetime import datetime
from typing import Optional

class TokenType(str, Enum):
    JWT_REFRESH = "refresh"
    JWT_ACCESS = "access"
    VERIFICATION = "verification"
    TWO_FACTOR = "two-factor"


class Token:
    def __init__(
        self, 
        code: str, 
        expires_at: datetime, 
        user_id: str, 
        type: TokenType, 
        is_revoked = False, 
        created_at: Optional[datetime] = datetime.now()
    ) -> None:
        self.code =  code
        self.expires_at =  expires_at
        self.user_id =  user_id
        self.type =  type
        self.is_revoked = is_revoked
        self.created_at = created_at
    
    def revoke(self):
        self.is_revoked = True
    
    

        