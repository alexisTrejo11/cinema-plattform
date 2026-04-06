from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class BaseToken(BaseModel):
    expires_at: datetime
    user_id: str
    type: str
    is_revoked: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    code: str = ""

    def revoke(self):
        self.is_revoked = True
    
    
class JWTToken(BaseToken):
    email: Optional[str] = None
    role: Optional[str] = None
    
    
class TwoFactorToken(BaseToken):
    pass

class ActivationToken(BaseToken):
    pass
