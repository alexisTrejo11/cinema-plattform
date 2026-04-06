from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import random

import jwt
import pyotp

from app.shared.token.core import TokenType, Token
from app.config.app_config import settings


def _encode_jwt(payload: dict) -> str:
    """Sign with app JWT settings; add aud/iss when configured (must match middleware decode)."""
    if settings.JWT_AUDIENCE is not None:
        payload["aud"] = settings.JWT_AUDIENCE
    if settings.JWT_ISSUER is not None:
        payload["iss"] = settings.JWT_ISSUER
    encoded = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded if isinstance(encoded, str) else encoded.decode("utf-8")


class StrategyToken(ABC):
    @abstractmethod
    def generate(self, **kwargs) -> Token:
        pass


class TokenRefreshJWT(StrategyToken):
    refresh_token_expire_days = 7

    def generate(self, **kwargs) -> Token:
        user_id = kwargs.get("user_id")
        role = kwargs.get("role")
        email = kwargs.get("email")
        token_type = TokenType.JWT_REFRESH
        expiration_date = datetime.now() + timedelta(
            days=self.refresh_token_expire_days
        )

        if not user_id:
            raise ValueError("user id required to creation activation token")

        jwt_payload = {
            "sub": str(user_id),
            "exp": int(expiration_date.timestamp()),
            "type": token_type.value,
        }

        if email:
            jwt_payload["email"] = str(email)
        if role is not None:
            jwt_payload["role"] = getattr(role, "value", role)

        token_code = _encode_jwt(jwt_payload)

        new_token = Token(
            code=token_code,
            user_id=str(user_id),
            type=token_type,
            expires_at=expiration_date,
        )

        return new_token


class TokenAccessJWT(StrategyToken):
    expire_minutes: int = 60

    def generate(self, **kwargs) -> Token:
        user_id = kwargs.get("user_id")
        token_type = TokenType.JWT_ACCESS
        expiration_date = datetime.now() + timedelta(minutes=self.expire_minutes)

        if not user_id:
            raise ValueError("user id required to creation activation token")

        jwt_payload = {
            "sub": str(user_id),
            "exp": int(expiration_date.timestamp()),
            "type": token_type.value,
        }

        token_code = _encode_jwt(jwt_payload)

        new_token = Token(
            code=token_code,
            user_id=str(user_id),
            type=token_type,
            expires_at=expiration_date,
        )
        return new_token


class TokenVerification(StrategyToken):
    expire_minutes: int = 60

    def generate(self, **kwargs) -> Token:
        user_id = kwargs.get("id", "")  # User Id
        token_code = ""
        for _ in range(6):
            token_code += f"{random.randint(1,9)}"

        expiration_date = datetime.now() + timedelta(minutes=self.expire_minutes)

        return Token(
            code=token_code,
            user_id=user_id,
            expires_at=expiration_date,
            type=TokenType.VERIFICATION,
        )


class Token2FASecret(StrategyToken):
    expire_minutes: int = 30

    def generate(self, **kwargs) -> Token:
        user_email = kwargs.get("email", "")

        totp_secret = pyotp.random_base32()
        return Token(
            code=totp_secret,
            expires_at=datetime.now() + timedelta(minutes=self.expire_minutes),
            user_id=user_email,
            type=TokenType.TWO_FACTOR_SECRET,
        )


class Token2FAAccess(StrategyToken):
    expire_minutes: int = 30
    issuer_name: str = "ATCinema"

    def generate(self, **kwargs) -> Token:
        user_email = kwargs.get("email")
        totp_secret = kwargs.get("totp_secret")

        if not user_email:
            raise ValueError("user email is required to generate 2FA access")

        if not totp_secret:
            raise ValueError("secret key is required to generate 2FA access")

        otp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(
            name=user_email, issuer_name=self.issuer_name
        )
        return Token(
            code=otp_uri,
            expires_at=datetime.now() + timedelta(minutes=self.expire_minutes),
            user_id=user_email,
            type=TokenType.TWO_FACTOR_SECRET,
        )


class CreateTokenStrategy:
    def __init__(self, strategy: StrategyToken) -> None:
        self.strategy = strategy

    def set_strategy(self, strategy: StrategyToken):
        self.strategy = strategy

    def create(self, **kwargs):
        return self.strategy.generate(**kwargs)


class TokenFactory:
    def create(self, token_type: TokenType, **kwargs) -> Token:
        match token_type:
            case TokenType.JWT_ACCESS:
                token_strategy = CreateTokenStrategy(TokenAccessJWT())
            case TokenType.JWT_REFRESH:
                token_strategy = CreateTokenStrategy(TokenRefreshJWT())
            case TokenType.VERIFICATION:
                token_strategy = CreateTokenStrategy(TokenVerification())
            case TokenType.TWO_FACTOR_SECRET:
                token_strategy = CreateTokenStrategy(Token2FASecret())
            case TokenType.TWO_FA:
                token_strategy = CreateTokenStrategy(Token2FAAccess())
            case _:
                raise ValueError("Token type not supported")

        token = token_strategy.create(**kwargs)
        return token
