from typing import TypeVar, Optional, Callable, Any, cast, TYPE_CHECKING
from functools import wraps
import inspect
from .serializer import SerializerService
import logging

if TYPE_CHECKING:
    from app.shared.redis.redis_service import RedisService


logger = logging.getLogger("app")

T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])


class CacheDecorator:

    def cache(self, key_template: str, ttl: int = 3600):
        def decorator(func: Callable[..., T]) -> Any:
            @wraps(func)
            async def wrapper(*args, **kwargs) -> Optional[T]:

                key = self._build_key(key_template, func, args, kwargs)
                cached = await RedisService.get(key)
                if cached is not None:
                    return SerializerService.deserialize(cached, func)

                if inspect.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)

                if result is not None:
                    await RedisService.save(key, result, ttl)
                return result

            return wrapper

        return decorator

    def _build_key(
        self,
        template: str,
        func: Callable,
        args: tuple,
        kwargs: dict,
        *,
        ignore_missing: bool = False,
    ) -> str:
        """
        Construye una clave de caché consistentemente.

        Args:
            template: Plantilla de formato (ej: "product:{product_id}")
            func: Función decorada (para obtener nombres de parámetros)
            args: Argumentos posicionales
            kwargs: Argumentos de palabra clave
            ignore_missing: Si True, omite parámetros faltantes en lugar de fallar
        """
        # Obtener información de parámetros
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        context = {
            **bound_args.arguments,
            "func_name": func.__name__,
            "class_name": (
                getattr(func, "__objclass__", type(args[0])).__name__ if args else None
            ),
        }

        try:
            return template.format(**context)
        except KeyError as e:
            if ignore_missing:
                from string import Formatter

                return "".join(
                    lit or f"{{{field}}}" if field not in context else f"{{{field}}}"
                    for lit, field, _, _ in Formatter().parse(template)
                )
            raise ValueError(f"Missing parameter '{e}' for cache key template") from e

    def invalidate_cache(
        self,
        key_template: str,
        pattern: bool = False,
    ) -> Callable[[F], F]:
        """
        Decorador para invalidar entradas de caché.

        Args:
            key_template: Plantilla para la clave a invalidar
            arg_name: Nombre del parámetro a usar en la plantilla
            arg_position: Posición del parámetro si no se pasa por nombre
            pattern: Si es True, usa el comando KEYS/PATTERN para búsqueda
        """

        def decorator(method: F) -> F:
            @wraps(method)
            async def async_wrapper(*args, **kwargs):
                return await _invalidate_wrapper(method, args, kwargs)

            @wraps(method)
            def sync_wrapper(*args, **kwargs):
                return _invalidate_wrapper(method, args, kwargs)

            async def _invalidate_wrapper(method: Callable, args: tuple, kwargs: dict):
                # Primero ejecutar el método
                if inspect.iscoroutinefunction(method):
                    result = await method(*args, **kwargs)
                else:
                    result = method(*args, **kwargs)

                # Construir contexto para formateo
                context = _build_context(method, args, kwargs)

                try:
                    cache_key = key_template.format(**context)

                    if pattern:
                        # Invalidar todas las claves que coincidan con el patrón
                        await RedisService.delete_pattern(cache_key)
                    else:
                        # Invalidar clave específica
                        await RedisService.delete(cache_key)

                except KeyError as e:
                    logger.warning(
                        f"Could not invalidate cache: missing key {e} in template"
                    )
                except Exception as e:
                    logger.error(f"Cache invalidation failed: {e}")

                return result

            return cast(
                F,
                async_wrapper if inspect.iscoroutinefunction(method) else sync_wrapper,
            )

        def _build_context(method: Callable, args: tuple, kwargs: dict) -> dict:
            """Construye el contexto para formatear las plantillas de clave."""
            context = {**kwargs}

            # Añadir argumentos posicionales por nombre
            param_names = method.__code__.co_varnames[1 : method.__code__.co_argcount]
            for name, arg in zip(param_names, args):
                context[name] = arg

            return context

        return decorator
