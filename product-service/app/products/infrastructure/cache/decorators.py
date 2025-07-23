from decimal import Decimal
from typing import (
    Concatenate,
    List,
    ParamSpec,
    Type,
    TypeVar,
    Optional,
    Callable,
    Any,
    Awaitable,
    Union,
)
from functools import wraps
from pydantic import BaseModel
import json
from config.redis import RedisManager
import logging
import uuid
from app.shared.schema import AbstractId

logger = logging.getLogger(__name__)

T = TypeVar("T")  # Tipo genérico sin restricciones


def cache_method(
    key_template: str,
    ttl: int = 3600,
    deserializer: Callable[[str, Type[T]], T] = lambda x, cls: cls(**json.loads(x)),
) -> Any:
    """
    Decorador que preserva los tipos para métodos async con self.
    """

    def decorator(
        method: Callable[Concatenate[Any, P], Awaitable[T]],
    ) -> Callable[Concatenate[Any, P], Awaitable[T]]:
        @wraps(method)
        async def wrapper(self: Any, *args: P.args, **kwargs: P.kwargs) -> T:
            redis = await RedisManager.get_client()

            format_context = {"self": self, **kwargs}

            # Añade argumentos posicionales por nombre si es posible
            param_names = method.__code__.co_varnames[1 : method.__code__.co_argcount]
            for name, arg in zip(param_names, args):
                format_context[name] = arg

            try:
                cache_key = key_template.format(**format_context)
            except KeyError as e:
                logger.error(f"Missing key for cache template: {e}")
                return await method(self, *args, **kwargs)
            except Exception as e:
                logger.error(f"Invalid cache key format: {e}")
                return await method(self, *args, **kwargs)

            # Try cache
            cached = await redis.get(cache_key)
            if cached:
                try:
                    return_type = method.__annotations__.get("return")
                    if (
                        hasattr(return_type, "__origin__")
                        and return_type.__origin__ is Union
                    ):
                        cls = return_type.__args__[0]  # Para Optional[Product]
                    else:
                        cls = return_type
                    return deserializer(cached, cls)
                except (json.JSONDecodeError, TypeError) as e:
                    logger.warning(f"Cache deserialization failed: {e}")

            # Call original method
            result = await method(self, *args, **kwargs)

            # Store in cache
            if result is not None:
                try:
                    await redis.set(cache_key, safe_serializer(result), ex=ttl)
                except (TypeError, ValueError) as e:
                    logger.error(f"Cache serialization failed: {e}")

            return result

        return wrapper

    return decorator


def invalidate_cache(
    key_template: str,
    arg_position: Optional[int] = None,
    arg_name: Optional[str] = None,
):
    """Decorator to invalidate cache for a method.
    Args:
        key_template (str): Template for the cache key to invalidate.
        arg_position (Optional[int]): Position of the argument to use in the key template.
        arg_name (Optional[str]): Name of the keyword argument to use in the key template.
    """

    def decorator(method: Callable[..., Any]):
        @wraps(method)
        async def wrapper(*args, **kwargs):
            if arg_name and arg_name in kwargs:
                arg_value = kwargs[arg_name]
            elif arg_position is not None and len(args) > arg_position:
                arg_value = args[arg_position]
            else:
                arg_value = None

            result = await method(*args, **kwargs)

            if arg_value is not None:
                cache_key = key_template.format(arg_value)
                redis_client = await RedisManager.get_client()

                await redis_client.delete(cache_key)

            return result

        return wrapper

    return decorator


P = ParamSpec("P")
T = TypeVar("T")
KT = TypeVar("KT")


def multi_key_cache(
    primary_key_template: str,
    related_key_templates: List[str] = None,
    ttl: int = 3600,
    batch_size: int = 100,
) -> Any:
    """
    Decorador avanzado para manejar caché con múltiples claves.

    Args:
        primary_key_template: Plantilla para la clave principal
        related_key_templates: Lista de plantillas para claves relacionadas
        ttl: Tiempo de vida en segundos
        batch_size: Tamaño de lote para operaciones masivas
    """

    def decorator(
        method: Callable[Concatenate[Any, P], Awaitable[T]],
    ) -> Callable[Concatenate[Any, P], Awaitable[T]]:
        @wraps(method)
        async def wrapper(self: Any, *args: P.args, **kwargs: P.kwargs) -> T:
            redis = await RedisManager.get_client()

            # Construir contexto para formato
            format_context = build_format_context(method, self, args, kwargs)

            try:
                # Clave principal
                primary_key = primary_key_template.format(**format_context)

                # Claves relacionadas
                related_keys = [
                    tpl.format(**format_context)
                    for tpl in (related_key_templates or [])
                ]

                # Intentar obtener de caché principal
                cached_data = await redis.get(primary_key)
                if cached_data:
                    try:
                        result = deserialize_with_type(cached_data, method)

                        # Verificar claves relacionadas si existen
                        if related_keys:
                            related_exists = await check_related_keys(
                                redis, related_keys
                            )
                            if all(related_exists):
                                return result
                    except (json.JSONDecodeError, TypeError) as e:
                        logger.warning(f"Cache deserialization failed: {e}")

                # Llamar al método original si no hay caché válido
                result = await method(self, *args, **kwargs)

                # Almacenar en caché si hay resultado
                if result is not None:
                    await store_with_relations(
                        redis, primary_key, related_keys, result, ttl, batch_size
                    )

                return result

            except Exception as e:
                logger.error(f"Cache operation failed: {e}")
                return await method(self, *args, **kwargs)

        return wrapper

    return decorator


def build_format_context(
    method: Callable, instance: Any, args: tuple, kwargs: dict
) -> dict:
    """Construye el contexto para formatear las plantillas de clave."""
    context = {"self": instance, **kwargs}

    # Añadir argumentos posicionales por nombre
    param_names = method.__code__.co_varnames[1 : method.__code__.co_argcount]
    for name, arg in zip(param_names, args):
        context[name] = arg

    return context


async def check_related_keys(redis, keys: List[str]) -> List[bool]:
    """Verifica la existencia de múltiples claves relacionadas."""
    return [await redis.exists(key) for key in keys]


async def store_with_relations(
    redis,
    primary_key: str,
    related_keys: List[str],
    value: Any,
    ttl: int,
    batch_size: int = 100,
) -> None:
    serialized = safe_serializer(value)

    async with redis.pipeline(transaction=True) as pipe:
        pipe.set(primary_key, serialized, ex=ttl)

        for key in related_keys:
            pipe.set(key, primary_key, ex=ttl)

        await pipe.execute()


def deserialize_with_type(data: str, method: Callable) -> Any:
    """Deserializa los datos teniendo en cuenta el tipo de retorno."""
    return_type = method.__annotations__.get("return")

    if hasattr(return_type, "__origin__"):
        if return_type.__origin__ is Union:  # Para Optional[Type]
            cls = return_type.__args__[0]
        elif return_type.__origin__ in (List, Set, Tuple):  # Para colecciones
            cls = return_type.__args__[0]
        else:
            cls = return_type
    else:
        cls = return_type

    return json.loads(data, object_hook=make_object_hook(cls))


def make_object_hook(cls: Type) -> Callable[[dict], Any]:
    """Crea un object_hook personalizado para la deserialización."""

    def hook(d: dict) -> Any:
        if cls is None:
            return d

        # Conversión especial para tipos conocidos
        if hasattr(cls, "from_cache_dict"):
            return cls.from_cache_dict(d)

        # Manejo de campos especiales
        for k, v in d.items():
            if isinstance(v, str):
                # Reconversión de UUID
                if k == "id" and hasattr(cls, "id"):
                    id_type = cls.__annotations__.get("id")
                    if hasattr(id_type, "__origin__") and id_type.__origin__ is UUID:
                        d[k] = UUID(v)
                # Reconversión de Decimal
                elif k in cls.__annotations__ and cls.__annotations__[k] is Decimal:
                    d[k] = Decimal(v)

        return cls(**d)

    return hook


def safe_serializer(obj: Any) -> str:
    """Serializador seguro para tipos complejos."""
    if obj is None:
        return json.dumps(None)

    if isinstance(obj, (list, tuple, set)):
        return json.dumps([safe_serializer_item(x) for x in obj])

    if hasattr(obj, "to_cache_dict"):
        return json.dumps(obj.to_cache_dict())

    if hasattr(obj, "__dict__"):
        data = {}
        for k, v in obj.__dict__.items():
            data[k] = safe_serializer_item(v)
        return json.dumps(data)

    return json.dumps(obj)


def safe_serializer_item(item: Any) -> Any:
    if isinstance(item, (uuid.UUID, AbstractId)):
        return str(item)
    elif isinstance(item, Decimal):
        return float(item)
    elif hasattr(item, "to_cache_dict"):
        return item.to_cache_dict()
    elif hasattr(item, "__dict__"):
        return {k: safe_serializer_item(v) for k, v in item.__dict__.items()}
    return item
