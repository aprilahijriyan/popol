from asyncio import iscoroutinefunction
from functools import wraps
from types import MethodType
from typing import Callable

from fastapi import Request

from ..utils import run_sync
from .backends.base import BaseCacheBackend
from .helpers import get_cache_backend, get_request_object
from .key import get_cache_key


def auto_connect(method: MethodType):
    """
    Decorator to ensure the backend cache is connected to the server.
    """
    if iscoroutinefunction(method):

        @wraps(method)
        async def wrapper(*args, **kwargs):
            self: BaseCacheBackend = args[0]
            if not self.client:
                await self.connect()
            return await method(*args, **kwargs)

    else:

        @wraps(method)
        def wrapper(*args, **kwargs):
            self: BaseCacheBackend = args[0]
            if not self.client:
                self.connect()
            return method(*args, **kwargs)

    return wrapper


def cached(
    timeout: int = 15,
    *,
    key: Callable[[Request], str] = get_cache_key,
    cache: str = "default"
) -> Callable:
    """
    Decorator to cache the result of a function.

    Args:
        timeout: Timeout in seconds.
        key: Function to generate the cache key.
        cache: The cache name.
    """

    assert callable(key), "key must be callable"

    def decorator(func: Callable) -> Callable:
        if iscoroutinefunction(func):

            @wraps(func)
            async def wrapper(*args, **kwargs):
                request = get_request_object(kwargs)
                if not request:
                    return await func(*args, **kwargs)

                cache_backend = get_cache_backend(request, cache)
                cache_key = key(request)
                cache_get = cache_backend.get
                if iscoroutinefunction(cache_get):
                    value = await cache_get(cache_key)
                else:
                    value = cache_get(cache_key)

                if value is None:
                    value = await func(*args, **kwargs)
                    cache_set = cache_backend.set
                    if iscoroutinefunction(cache_set):
                        await cache_set(cache_key, value, timeout)
                    else:
                        cache_set(cache_key, value, timeout)

                return value

        else:

            @wraps(func)
            def wrapper(*args, **kwargs):
                request = get_request_object(kwargs)
                if not request:
                    return func(*args, **kwargs)

                cache_backend = get_cache_backend(request, cache)
                cache_key = key(request)
                cache_get = cache_backend.get
                if iscoroutinefunction(cache_get):
                    value = run_sync(cache_get, cache_key)
                else:
                    value = cache_get(cache_key)

                if value is None:
                    value = func(*args, **kwargs)
                    cache_set = cache_backend.set
                    if iscoroutinefunction(cache_set):
                        run_sync(cache_set, cache_key, value, timeout)
                    else:
                        cache_set(cache_key, value, timeout)

                return value

        return wrapper

    return decorator
