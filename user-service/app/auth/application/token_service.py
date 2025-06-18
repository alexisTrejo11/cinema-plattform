from typing import Optional, Any, Dict
from datetime import datetime
from app.auth.domain.entities import JWTToken
from abc import abstractmethod, ABC

class TokenService(ABC):
    """
    Abstract base class defining the interface for a generic token service.
    This service handles the creation and verification of application tokens.
    """

    def __init__(self, access_token_expire_minutes: int, refresh_token_expire_days: int):
        """
        Initializes the abstract token service with common configuration.
        Concrete implementations will handle technology-specific parameters.
        """
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    @abstractmethod
    def create_token( self, user_id: str, email: Optional[str] = None, role: Optional[str] = None, is_access_token: bool = True) -> JWTToken:
        """
        Creates a new application token (access or refresh) for a given user.
        The specific format of the token (e.g., JWT string) is an implementation detail.

        Args:
            user_id (str): The ID of the user for whom the token is created.
            email (Optional[str]): The user's email, to be included in the token payload.
            role (Optional[str]): The user's role, to be included in the token payload.
            is_access_token (bool): True for an access token, False for a refresh token.

        Returns:
            JWTToken: An object containing the token details (including the raw token string).
        """
        pass

    @abstractmethod
    def verify_token(self, token_string: str) -> Dict[str, Any]:
        """
        Verifies an application token string and returns its decoded payload.
        The specific verification mechanism is an implementation detail.

        Args:
            token_string (str): The raw encoded token string.

        Returns:
            Dict[str, Any]: The decoded token payload (e.g., user_id, type, expiry).

        Raises:
            InvalidCredentialsException: If the token is invalid, expired, or verification fails.
        """
        pass

    @abstractmethod
    def _get_token_expiration_date(self, is_access_token: bool) -> datetime:
        """
        Abstract method to determine the expiration date for a token based on its type.
        This allows concrete implementations to define their own precise expiration logic
        (e.g., timezone handling).
        """
        pass