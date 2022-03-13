from inspect import iscoroutinefunction
from typing import Any, Dict, List

from fastapi import FastAPI

from ..utils import get_settings, import_attr
from .backends.base import BaseCacheBackend
from .backends.dummy import DummyBackend
from .serializers.base import BaseSerializer


def setup(app: FastAPI, settings: Any = None) -> Dict[str, BaseCacheBackend]:
    """
    Install the cache plugin to the app.
    This will attach 2 attributes to `app.state` i.e:

    * `cache` - Default cache backend if available.
    * `caches` - All cache backends (dict type)

    Args:
        app: FastAPI app.
        settings: The settings (can be pydantic.BaseSettings).

    Returns:
        Dict[str, popol.cache.backends.base.BaseCacheBackend]: cache backends.
    """
    settings = get_settings(app, settings)
    caches = {}
    caches_settings: Dict[str, dict] = getattr(settings, "CACHES", {})
    for name, cache_config in caches_settings.items():
        serializer_settings: dict = cache_config.get("serializer", {})
        serializer_class = serializer_settings.get(
            "class", "popol.cache.serializers.PickleSerializer"
        )
        serializer_options: dict = serializer_settings.get("options", {})
        try:
            serializer_class: BaseSerializer = import_attr(serializer_class)
        except ImportError as e:
            raise ImportError(
                f"Could not import serializer class {serializer_class}"
            ) from e

        serializer = serializer_class(
            serializer_options.get("dumps", {}),
            serializer_options.get("loads", {}),
        )
        backend = cache_config.get("backend")
        if not backend:
            raise RuntimeError('No backend specified for cache "{}"'.format(name))

        try:
            backend = import_attr(backend)
        except ImportError as e:
            raise RuntimeError(
                'Could not import cache backend "{}"'.format(backend)
            ) from e

        options = cache_config.get("options", {})
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
