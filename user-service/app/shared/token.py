from enum import Enum
from datetime import datetime


class TokenType(Enum,str):
    JWT_REFRESH = "JWT_REFRESH"
    JWT_ACCESS = "JWT_REFRESH"
    ACTIVATION = "ACTIVATION"


class Token:
    def __init__(self, code: str, expires_at: datetime, user_id: str, type: TokenType) -> None:
        self.__code =  code
        self.__expires_at =  expires_at
        self.__user_id =  user_id
        self.__type =  type
        self.__is_revoked = False
        self.__created_at =  datetime.now()
    
    def revoke(self):
        self.__is_revoked = True
    
    @property
    def is_revoked(self):
        return self.__is_revoked
    
    @property
    def expires_at(self):
        return self.__expires_at
    
    @property
    def type(self):
        return self.__type
    
    @property
    def user_id(self):
        return self.__user_id
    
    @property
    def code(self):
        return self.__code
    
    @property
    def created_at(self):
        return self.__created_at
    
    