import uuid
from dataclasses import dataclass

@dataclass(frozen=True)
class ID:
    value: uuid.UUID

    def __str__(self):
        return str(self.value)

    @staticmethod
    def generate():
        return ID(uuid.uuid4())

