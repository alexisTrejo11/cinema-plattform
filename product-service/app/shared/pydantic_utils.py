"""
Utilities for making value objects compatible with Pydantic and FastAPI.
"""
from typing import Any, Type, TypeVar, get_origin, get_args
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from pydantic._internal._generate_schema import GenerateSchema
from pydantic._internal._config import ConfigWrapper

from app.promotions.domain.valueobjects import PromotionId
from app.products.domain.entities.value_objects import ProductId
from app.shared.schema import AbstractId

T = TypeVar('T', bound=AbstractId)


def validate_id_field(value: Any, id_class: Type[T]) -> T:
    """Validate and convert a value to an ID value object."""
    if isinstance(value, id_class):
        return value
    elif isinstance(value, str):
        return id_class.from_string(value)
    elif hasattr(value, 'value'):  # Handle other ID types
        return id_class(value.value)
    else:
        raise ValueError(f"Cannot convert {type(value)} to {id_class.__name__}")


def serialize_id_field(value: AbstractId) -> str:
    """Serialize an ID value object to string."""
    return str(value.value)


class PromotionIdPydanticAnnotation:
    """Pydantic annotation for PromotionId."""
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Any,
    ) -> core_schema.CoreSchema:
        """Define the core schema for PromotionId."""
        return core_schema.no_info_after_validator_function(
            lambda x: validate_id_field(x, PromotionId),
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """Define the JSON schema for PromotionId."""
        return handler(core_schema.str_schema())


class ProductIdPydanticAnnotation:
    """Pydantic annotation for ProductId."""
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Any,
    ) -> core_schema.CoreSchema:
        """Define the core schema for ProductId."""
        return core_schema.no_info_after_validator_function(
            lambda x: validate_id_field(x, ProductId),
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """Define the JSON schema for ProductId."""
        return handler(core_schema.str_schema())


# Type aliases for easier use
PromotionIdField = PromotionIdPydanticAnnotation
ProductIdField = ProductIdPydanticAnnotation
