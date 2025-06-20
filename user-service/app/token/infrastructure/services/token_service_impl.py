from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError, JWTError 
from app.auth.domain.exceptions import InvalidCredentialsException
from app.token.application.service import TokenService
from app.token.domain.token import TokenType, Token
from ..repository.token_repository import TokenRepository
from ..strategy_token import TokenAccessJWT, TokenVerification, TokenRefreshJWT, CreateToken
import os
import logging

logger = logging.getLogger("app")


class TokenServiceImpl(TokenService):
    def __init__(self, token_repository: TokenRepository) -> None:
        self.token_repository = token_repository
        super().__init__()
        

    def create(self, token_type: TokenType , **kwargs) -> Token:
        if token_type == TokenType.JWT_ACCESS:
            token_strategy = CreateToken(TokenAccessJWT())
            
            token = token_strategy.create(**kwargs)
        elif token_type == TokenType.JWT_REFRESH:
            token_strategy = CreateToken(TokenRefreshJWT())
            
            token = token_strategy.create(**kwargs)           
        elif token_type == TokenType.VERIFICATION:
            token_strategy = CreateToken(TokenVerification())
            
            token = token_strategy.create(**kwargs)       
        else:
            raise ValueError("Token type not supported")
        
        self.token_repository.create(token)
        return token

    def verify_token(self, token_string: str, token_type: TokenType, user_id: int) -> bool:
        if token_type in [TokenAccessJWT, TokenAccessJWT]:
            self._validate_jwt_token(token_string)
        
        if token_type not in [TokenAccessJWT, TokenVerification]:
            token = self.token_repository.get_user_token(str(user_id), token_string, token_type)
            if not token:
                return False
            
            if token.is_revoked or token.expires_at > datetime.now():
                return False
            
        return True
    

    def _validate_jwt_token(self, token_str : str):
        try:
            payload = jwt.decode(token_str, os.getenv("SECRET_KEY", ""), algorithms=[os.getenv("ALGORITHM", "")])
            return True
        except ExpiredSignatureError as e:
            logger.error(f"(verify_token): Token expired: {e}")
            raise InvalidCredentialsException("Token has expired")
        except JWTError as e:
            logger.error(f"(verify_token): General JOSE JWTError: {e}")
            raise InvalidCredentialsException(f"Invalid token: {e}")
        except Exception as e:
            logger.error(f"(verify_token): Unexpected error during token verification: {type(e).__name__}: {e}")
            raise InvalidCredentialsException(f"Token verification failed unexpectedly: {e}")
        

    def get_by_code_user_and_type(self, user_id: str, token_string: str, token_type: TokenType) -> Optional[Token]:
        token = self.token_repository.get_user_token(user_id, token_string, token_type)
        if token and not token.is_revoked:
            return token

        return None
        
    def revoke(self, user_id: str, token_type: TokenType, token_string: str) -> bool:
        token = self.token_repository.get_user_token(user_id, token_string, token_type)
        if not token or token.is_revoked:
            return False
         
        self.token_repository.revoke_user_token(user_id, token_string, token_type)
        return True
        
    def revoke_all_refresh_by_user(self, user_id: str) -> None:
           self.token_repository.revoke_all_user_tokens(user_id)
