from fastapi import Request

from .backends.base import BaseCacheBackend


def get_request_object(kwargs: dict) -> Request:
    request: Request = None
    for _, v in kwargs.items():
        if isinstance(v, Request):
            request = v
            break

    return request


def get_cache_backend(request: Request, cache: str = "default") -> BaseCacheBackend:
    cache_backend: BaseCacheBackend = request.app.state.caches[cache]
    return cache_backend
