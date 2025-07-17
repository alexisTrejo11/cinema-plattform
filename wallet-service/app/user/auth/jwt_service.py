from typing import Dict, Any, Optional
from datetime import datetime
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError, JWTError 
from app.shared.base_exceptions import AuthorizationException
import logging


logger = logging.getLogger("app")

class JWTTokenService:
    def __init__(self, secret_key : str, algorithm : str) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        super().__init__()

    
    def verify_jwt_token(self, token_string : str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token_string, self.secret_key, algorithms=[self.algorithm])
            return payload
        except ExpiredSignatureError as e:
            logger.error(f"(verify_token): Token expired: {e}")
            raise AuthorizationException("Token has expired")
        except JWTError as e:
            logger.error(f"(verify_token): General JOSE JWTError: {e}")
            raise AuthorizationException(f"Invalid token: {e}")
        except Exception as e:
            logger.error(f"(verify_token): Unexpected error during token verification: {type(e).__name__}: {e}")
            raise AuthorizationException(f"Token verification failed unexpectedly: {e}")

