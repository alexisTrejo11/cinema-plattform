import re
from pydantic import Field
from typing import Any, Optional
from datetime import datetime
from .enums import UserRole, Status
from .exceptions import PasswordValidationError
from .valueobjects import UserEmail, PhoneNumber, RawPassword, TotpSecret
from app.profile.application.dtos import Profile


class Account(Profile):
    email: UserEmail
    phone_number: Optional[PhoneNumber] = None
    password: RawPassword
    role: UserRole = UserRole.CUSTOMER
    status: Status = Status.PENDING
    totp_secret: Optional[TotpSecret] = None
    is_2fa_enabled: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class User(Account):
    id: int = 0

    def update_profile(self, **kwargs: Any) -> None:
        """
        Updates the user's profile information based on provided keyword arguments.
        Only updates fields that are explicitly present in kwargs.
        """
        updatable_fields = [
            "email",
            "gender",
            "phone_number",
            "first_name",
            "last_name",
            "date_of_birth",
        ]

        for field_name in updatable_fields:
            if field_name in kwargs:
                new_value = kwargs[field_name]

                setattr(self, field_name, new_value)

        self.updated_at = datetime.now()

    def add_2FA_config(self, secret: str) -> None:
        self.is_2fa_enabled = True
        self.totp_secret = secret

    def disable_2FA_config(self) -> None:
        self.is_2fa_enabled = False
        self.totp_secret = None

    def update_password(self, new_password: str) -> None:
        self.password = new_password
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        self.status = Status.INACTIVE
        self.updated_at = datetime.now()

    def activate(self) -> None:
        self.status = Status.ACTIVE
        self.updated_at = datetime.now()

    def ban(self) -> None:
        self.status = Status.BANNED
        self.updated_at = datetime.now()

    @staticmethod
    def validate_password_before_hash(password: str):
        """
        Validates if a given password meets the strong password criteria using regular expressions.

        Criteria:
        - Minimum 8 characters in length.
        - Contains at least one uppercase letter.
        - Contains at least one lowercase letter.
        - Contains at least one digit.
        - Contains at least one special character from the set: !@#$%^&*()_+-=[]{}|;:'",.<>/?~

        Args:
            password (str): The password string to validate.

        Raise:
            PasswordValidationError

        Returns:
            None
        """
        password_regex = re.compile(
            r"""
            (?=.*[a-z])
            (?=.*[A-Z])(?=.*\d)
            (?=.*[!@#$%^&*()_+\-=\[\]{}|;:'",.<>/?~])
            .{8,}
            $
            """,
            re.VERBOSE,
        )

        if not password_regex.fullmatch(password):
            raise PasswordValidationError("Password", "not strong enough")


__all__ = [
    "Account",
    "User",
]
