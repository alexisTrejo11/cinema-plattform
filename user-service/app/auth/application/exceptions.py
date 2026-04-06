from typing import Any, Dict
from http import HTTPStatus
from app.shared.exceptions import AuthorizationException, ValidationException

class UserNotActivatedError(AuthorizationException):
    def __init__(
        self, 
        details: Dict[str, Any] | None = None
        ):
        self.message = "User Account Has Not Been Activated. Check Your Email or Request an Activation Token."
        self.error_code = "USER_NOT_ACTIVATED"
        super().__init__( self.message, self.error_code, details)
        
    status_code = HTTPStatus.CONFLICT
    

class UserBannedError(AuthorizationException):
    def __init__(
        self, 
        details: Dict[str, Any] | None = None
        ):
        self.message = "User Account Has Not Been Banned."
        self.error_code = "USER_BANNED"
        super().__init__(self.message, self.error_code, details)
        
    status_code = HTTPStatus.CONFLICT
    
    
class InvalidAuthToken(ValidationException):
   def __init__(self, field: str, reason: str):
       super().__init__(field, reason)
        
