from abc import ABC, abstractmethod
from app.token.domain.token import TokenType, Token
from jose import JWTError, jwt
from datetime import datetime, timedelta
import random
import os

class StrategyToken(ABC):
    @abstractmethod
    def generate(self, **kwargs) -> Token:
        pass
    

class TokenRefreshJWT(StrategyToken):
    secret_key = os.getenv("SECRET_KEY", "")
    algorithm = "HS256"
    refresh_token_expire_days = 7
            
    def generate(self,  **kwargs) -> Token:
        user_id = kwargs.get('user_id')
        role = kwargs.get('role')
        email = kwargs.get('email') 
        token_type = TokenType.JWT_REFRESH
        expiration_date = datetime.now() + timedelta(days=self.refresh_token_expire_days)
        
        if not user_id:
            raise ValueError("user id required to creation activation token")
        
        jwt_payload = {
            "sub": user_id, 
            "exp": int(expiration_date.timestamp()), 
            "type": token_type
        }
        
        if email:
            jwt_payload["email"] = email
        if role:
            jwt_payload["role"] = role

        token_code = jwt.encode(jwt_payload, self.secret_key, algorithm=self.algorithm)

        new_token = Token(
            code=token_code,
            user_id=user_id, 
            type=token_type, 
            expires_at=expiration_date
        )
         
        return new_token


class TokenAccessJWT(StrategyToken):
    secret_key = os.getenv("SECRET_KEY", "")
    algorithm = "HS256"
    expire_minutes: int = 60
    
    def generate(self,  **kwargs) -> Token:
        user_id = kwargs.get('user_id')
        token_type = TokenType.JWT_ACCESS
        expiration_date = datetime.now() + timedelta(minutes=self.expire_minutes)
        
        if not user_id:
            raise ValueError("user id required to creation activation token")
        
        jwt_payload = {
            "sub": user_id, 
            "exp": int(expiration_date.timestamp()), 
            "type": token_type
        }
        
        token_code = jwt.encode(jwt_payload, self.secret_key, algorithm=self.algorithm)

        new_token = Token(
            code=token_code,
            user_id=user_id, 
            type=token_type, 
            expires_at=expiration_date
        )
         
        return new_token


class TokenVerification(StrategyToken):
    expire_minutes: int = 60
    
    def generate(self, **kwargs) -> Token:
        user_id = kwargs.get('id') #User Id
        if not user_id:
            raise ValueError("id required to creation activation token")
        
        token_code = ""
        for _ in range(6):
          token_code += f"{random.randint(1,9)}"

        expiration_date = datetime.now() + timedelta(minutes=self.expire_minutes)
        
        return Token( 
            code=token_code,
            user_id=user_id,
            expires_at=expiration_date,
            type=TokenType.VERIFICATION
        )
    
        
class CreateToken:
    def __init__(self, strategy: StrategyToken) -> None:
        self.strategy = strategy
        
    def set_strategy(self, strategy: StrategyToken):
        self.strategy = strategy
    
    def create(self, **kwargs):
        return self.strategy.generate(**kwargs)