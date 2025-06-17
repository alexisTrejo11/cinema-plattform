from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError, JWTError 
from app.auth.domain.entities import TokenType, JWTToken
from app.auth.domain.exceptions import InvalidCredentialsException

class JWTService:
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 15,
        refresh_token_expire_days: int = 7
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days


    def create_token(
        self,
        user_id: str,
        email: Optional[str] = None,
        role: Optional[str] = None,
        is_access_token: bool = True
    ) -> JWTToken:

        expire_date = self._get_token_expiration_date(is_access_token)
        new_token = JWTToken(
            user_id=user_id,
            type=TokenType.JWT_ACCESS if is_access_token else TokenType.JWT_REFRESH,
            expires_at=expire_date,
            role=role,
            email=email,
        )

        payload: Dict[str, Any] = {
            "sub": new_token.user_id,
            "exp": int(new_token.expires_at.timestamp()),
            "type": new_token.type.value,
        }

        if new_token.email:
            payload["email"] = new_token.email
        if new_token.role:
            payload["role"] = new_token.role

        print(f"DEBUG (create_token): Payload for JWT encoding: {payload}")

        token_code = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

        new_token.code = token_code
        return new_token


    def _get_token_expiration_date(self, is_access_token: bool) -> datetime:
        if is_access_token:
            return datetime.now() + timedelta(minutes=self.access_token_expire_minutes)
        else:
            return datetime.now() + timedelta(days=self.refresh_token_expire_days)


    def verify_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            print(f"DEBUG (verify_token): Successfully decoded payload: {payload}")
            return payload
        except ExpiredSignatureError as e:
            print(f"DEBUG (verify_token): Token expired: {e}")
            raise InvalidCredentialsException("Token has expired")
        except JWTError as e:
            print(f"DEBUG (verify_token): General JOSE JWTError: {e}")
            raise InvalidCredentialsException(f"Invalid token: {e}")
        except Exception as e:
            print(f"DEBUG (verify_token): Unexpected error during token verification: {type(e).__name__}: {e}")
            raise InvalidCredentialsException(f"Token verification failed unexpectedly: {e}")
