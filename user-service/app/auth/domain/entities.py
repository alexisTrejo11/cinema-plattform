from enum import Enum
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional




@dataclass(kw_only=True)
class BaseToken:
    expires_at: datetime
    user_id: str
    type: str
    is_revoked: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    code: str = field(default="")

    def revoke(self):
        self.is_revoked = True
    
    
@dataclass(kw_only=True)
class JWTToken(BaseToken):
    email: Optional[str] = None
    role: Optional[str] = None
    
    
@dataclass
class TwoFactorToken(BaseToken):
    pass

@dataclass
class ActivationToken(BaseToken):
    pass