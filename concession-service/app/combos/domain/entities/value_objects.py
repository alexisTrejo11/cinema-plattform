import uuid

from app.shared.schema import PydanticUUID


class ComboId(PydanticUUID):
    pass


class ComboItemId(PydanticUUID):
    @classmethod
    def generate(cls) -> "ComboItemId":
        return cls.model_construct(value=uuid.uuid4())

    @classmethod
    def from_string(cls, value: str) -> "ComboItemId":
        try:
            return cls.model_construct(value=uuid.UUID(value))
        except ValueError:
            raise ValueError("Invalid UUID string format")
