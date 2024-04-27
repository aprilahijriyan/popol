import time
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

import pytest
import asyncio
import timeit

from asgi_lifespan import LifespanManager
from popol import cache
from popol.cache.backends.redis import RedisBackend, AsyncRedisBackend
from popol.cache.decorators import cached
from popol.cache.globals import cache as default_cache_backend, caches
from popol.context.proxy import LocalProxy

default_cache_backend: RedisBackend
async_cache_backend: AsyncRedisBackend = LocalProxy(lambda: caches["aioredis"])


@pytest.fixture
def cache_app(app: FastAPI):
    cache.setup(app)

    async def root(request: Request):
        await asyncio.sleep(5)
        return {"message": "Hello World"}

    def sync_version(request: Request):
        time.sleep(5)
        return {"message": "Hello World"}

    app.add_api_route("/", cached(15)(root))
    app.add_api_route("/async", cached(15, cache="aioredis")(sync_version))
    return app


@pytest.fixture
async def cache_client(cache_app: FastAPI):
    async with LifespanManager(cache_app):
        default_cache_backend.connect()
        with TestClient(cache_app) as client:
            yield client


@pytest.mark.anyio
@pytest.mark.parametrize("path", ["/", "/async"])
async def test_cache_via_api(path: str, cache_client: TestClient):
    def _run_test(path: str):
        start_time = timeit.default_timer()
        response = cache_client.get(path)
        end_time = timeit.default_timer()
        elapsed_time = int(end_time - start_time)
        return response, elapsed_time

    # First request will take 5 seconds or more than that.
    response, elapsed_time = _run_test(path)
    assert response.status_code == 200 and elapsed_time >= 5
    # Second request will be fast under 5 seconds.
    response, elapsed_time = _run_test(path)
    assert response.status_code == 200 and elapsed_time < 5

def test_sync_redis_backend():
    assert isinstance(default_cache_backend, RedisBackend)
    key = "test"
    with default_cache_backend as cache:
        cache.delete(key)
        assert cache.get(key) is None
        cache.set(key, 1)
        assert cache.get(key) == 1
        assert cache.incr(key) == 2
        assert cache.decr(key) == 1
        cache.clear()

@pytest.mark.anyio
async def test_async_redis_backend():
    assert isinstance(async_cache_backend, AsyncRedisBackend)
    key = "test"
    async with async_cache_backend as cache:
        await cache.delete(key)
        assert await cache.get(key) is None
        await cache.set(key, 1)
        assert await cache.get(key) == 1
        assert await cache.incr(key) == 2
        assert await cache.decr(key) == 1
        await cache.clear()
