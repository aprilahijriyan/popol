from typing import Dict

from popol.context.globals import state
from popol.context.proxy import LocalProxy

from .backends.base import BaseCacheBackend

cache: BaseCacheBackend = LocalProxy(lambda: state.cache)
caches: Dict[str, BaseCacheBackend] = LocalProxy(lambda: state.caches)
