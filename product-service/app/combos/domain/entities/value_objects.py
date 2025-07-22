from uuid import UUID
import uuid
from typing import Any
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from app.shared.schema import AbstractId


class ComboId(AbstractId):
    pass


class ComboItemId(AbstractId):
    pass
