from typing import List
from datetime import datetime
from pydantic import BaseModel
from ..value_objects import UserId


class User(BaseModel):
    id: UserId
    name: str
    email: str
    phone: str
    roles: List[str]
    created_at: datetime
    updated_at: datetime
