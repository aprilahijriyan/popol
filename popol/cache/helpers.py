from fastapi import Request

from .backends.base import BaseCacheBackend


def get_request_object(kwargs: dict) -> Request:
    """
    Function to retrieve Request object in parameter if available.
    """
    request: Request = None
    for _, v in kwargs.items():
        if isinstance(v, Request):
            request = v
            break

    return request


def get_cache_backend(request: Request, cache: str = "default") -> BaseCacheBackend:
    """
    Get specific backend cache by name.

    Args:
        request: The request object.
        cache: The cache name.
    """
    cache_backend: BaseCacheBackend = request.app.state.caches[cache]
    return cache_backend
