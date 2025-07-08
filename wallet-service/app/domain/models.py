
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class User(BaseModel):
    """
    Represents a user in the domain.
    """
    id: UUID = Field(default_factory=uuid4)
    username: str = Field(..., description="The user's username.")
    email: str = Field(..., description="The user's email address.")

class Wallet(BaseModel):
    """
    Represents a wallet in the domain.
    """
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID = Field(..., description="The ID of the user who owns the wallet.")
    balance: float = Field(0.0, ge=0, description="The wallet balance, which cannot be negative.")

