from dataclasses import asdict, is_dataclass
from datetime import datetime
from decimal import Decimal
import json
from typing import Any, Callable, List, Set, Tuple, Type, Union
import uuid
from app.shared.schema import AbstractId


class SerializerService:
    @classmethod
    def serialize(cls, obj: Any) -> str:
        if obj is None:
            return json.dumps(None)

        if isinstance(obj, (str, int, float, bool)):
            return json.dumps(obj)

        if isinstance(obj, datetime):
            return json.dumps(obj.isoformat())

        if is_dataclass(obj):
            return json.dumps(asdict(obj))

        if hasattr(obj, "to_dict"):
            return json.dumps(cls._serialize_dict(obj.to_dict()))

        if hasattr(obj, "__dict__"):
            return json.dumps(cls._serialize_dict(obj.__dict__))

        raise ValueError(f"Cannot serialize object of type {type(obj)}")

    @classmethod
    def _serialize_dict(cls, data: dict) -> dict:
        return {k: cls._serialize_value(v) for k, v in data.items()}

    @classmethod
    def _serialize_value(cls, value: Any) -> Any:
        if isinstance(value, AbstractId):
            return value.to_string()
        if isinstance(value, (uuid.UUID)):
            return str(value)
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, (list, tuple, set)):
            return [cls._serialize_value(v) for v in value]
        if hasattr(value, "__dict__"):
            return cls._serialize_dict(value.__dict__)
        return value

    @classmethod
    def deserialize(cls, data: str, method: Callable) -> Any:
        """Deserializa los datos teniendo en cuenta el tipo de retorno."""
        return_type = method.__annotations__.get("return")

        if hasattr(return_type, "__origin__"):
            if return_type:
                if return_type.__origin__ is Union:
                    method_cls = return_type.__args__[0]
                elif return_type.__origin__ in (List, Set, Tuple):
                    method_cls = return_type.__args__[0]
                else:
                    method_cls = return_type
        else:
            method_cls = return_type

        return json.loads(data, object_hook=make_object_hook(method_cls))


def make_object_hook(cls: Type) -> Callable[[dict], Any]:
    """Crea un object_hook personalizado para la deserialización."""

    def hook(d: dict) -> Any:
        if cls is None:
            return d

        # Conversión especial para tipos conocidos
        if hasattr(cls, "from_dict"):
            return cls.from_dict(d)

        # Manejo de campos especiales
        for k, v in d.items():
            if isinstance(v, str):
                # Reconversión de UUID
                if k == "id" and hasattr(cls, "id"):
                    id_type = cls.__annotations__.get("id")
                    if (
                        hasattr(id_type, "__origin__")
                        and id_type.__origin__ is uuid.UUID
                    ):
                        d[k] = uuid.UUID(v)
                # Dates reconversion
                elif k == "created_at" and hasattr(cls, "created_at"):
                    d[k] = datetime.fromisoformat(v)

                elif k == "updated_at" and hasattr(cls, "updated_at"):
                    d[k] = datetime.fromisoformat(v)
                # Reconversión de Decimal
                elif k in cls.__annotations__ and cls.__annotations__[k] is Decimal:
                    d[k] = Decimal(v)

        return cls(**d)

    return hook
