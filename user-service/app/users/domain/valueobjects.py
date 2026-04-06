from typing import Annotated

from pydantic import EmailStr, Field, StringConstraints

UserEmail = EmailStr
PhoneNumber = Annotated[str, StringConstraints(min_length=6, strip_whitespace=True)]
RawPassword = Annotated[str, StringConstraints(min_length=8)]
TotpSecret = Annotated[str, Field(min_length=6)]

__all__ = [
    "UserEmail",
    "PhoneNumber",
    "RawPassword",
    "TotpSecret",
]
