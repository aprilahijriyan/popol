from inspect import iscoroutinefunction
from typing import Any, Dict, List

from fastapi import FastAPI

from ..utils import get_settings, import_attr
from .backends.base import BaseCacheBackend
from .backends.dummy import DummyBackend
from .serializers.base import BaseSerializer


def setup(app: FastAPI, settings: Any = None) -> Dict[str, BaseCacheBackend]:
    settings = get_settings(app, settings)
    caches = {}
    caches_settings: Dict[str, dict] = getattr(settings, "CACHES", {})
    for name, cache_config in caches_settings.items():
        serializer_settings: dict = cache_config.get("SERIALIZER", {})
        serializer_class = serializer_settings.get(
            "CLASS", "popol.cache.serializers.PickleSerializer"
        )
        serializer_options: dict = serializer_settings.get("OPTIONS", {})
        try:
            serializer_class: BaseSerializer = import_attr(serializer_class)
        except ImportError as e:
            raise ImportError(
                f"Could not import serializer class {serializer_class}"
            ) from e

        serializer = serializer_class(
            serializer_options.get("DUMPS", {}),
            serializer_options.get("LOADS", {}),
        )
        backend = cache_config.get("BACKEND")
        if not backend:
            raise RuntimeError('No backend specified for cache "{}"'.format(name))

        try:
            backend = import_attr(backend)
        except ImportError as e:
            raise RuntimeError(
                'Could not import cache backend "{}"'.format(backend)
            ) from e

        options = cache_config.get("OPTIONS", {})
        backend = backend(serializer, **options)
        caches[name] = backend

    app.state.caches = caches
    default_cache = caches.get("default")
    if not default_cache:
        default_cache = DummyBackend(None)

    app.state.cache = default_cache

    async def on_shutdown():
        caches: List[BaseCacheBackend] = app.state.caches.values()
        for cache in caches:
            method = cache.disconnect
            if iscoroutinefunction(method):
                await method()
            else:
                method()

    app.add_event_handler("shutdown", on_shutdown)
    return caches
