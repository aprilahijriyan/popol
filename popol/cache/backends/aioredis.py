from datetime import timedelta
from typing import Any, Optional, Union

from ..decorators import auto_connect
from ..serializers.base import BaseSerializer
from .base import BaseCacheBackend

try:
    from aioredis.client import Pipeline, Redis
    from aioredis.lock import Lock

except ImportError:
    errMsg = "aioredis is not installed. Please install it with `pip install aioredis`"
    raise RuntimeError(errMsg)


class AsyncRedisBackend(BaseCacheBackend):
    """
    aioredis cache backend.
    """

    def __init__(self, serializer: BaseSerializer, **kwargs):
        """
        Initialize the Redis cache.
        """

        super().__init__(serializer, **kwargs)
        self.client: Optional[Redis] = None

    async def connect(self, **kwargs) -> "AsyncRedisBackend":
        """
        Create a connection to the Redis server.
        """

        if self.client:
            return self.client

        kwargs.update(self.kwargs)
        self.client = Redis(**kwargs)
        await self.client.initialize()
        return self

    async def disconnect(self) -> None:
        """
        Disconnect from the Redis server.
        """

        if self.client:
            await self.client.close()
            self.client = None

    @auto_connect
    async def get(self, key: str) -> Any:
        """
        Get a value from the cache.
        """

        value = await self.client.get(key)
        if value:
            return self.serializer.loads(value)
        return value

    @auto_connect
    async def set(
        self, key: str, value: Any, timeout: Optional[Union[int, timedelta]] = None
    ) -> None:
        """
        Set a value in the cache.
        """

        value = self.serializer.dumps(value)
        if timeout:
            await self.client.setex(key, timeout, value)
        else:
            await self.client.set(key, value)

    @auto_connect
    async def delete(self, key: str) -> None:
        """
        Delete a value from the cache.
        """
        await self.client.delete(key)

    @auto_connect
    async def clear(self) -> None:
        """
        Clear the entire cache.
        """
        await self.client.flushdb()

    @auto_connect
    async def incr(self, name: str, amount: int = 1) -> int:
        """
        Increment the value of an integer cached key.
        """
        return await self.client.incr(name, amount)

    @auto_connect
    async def decr(self, name: str, amount: int = 1) -> int:
        """
        Decrement the value of an integer cached key.
        """
        return await self.client.decr(name, amount)

    @auto_connect
    def pipeline(self, **kwds) -> Pipeline:
        return self.client.pipeline(**kwds)

    @auto_connect
    def lock(self, name: str, **kwds) -> Lock:
        return self.client.lock(name, **kwds)

    async def __aenter__(self) -> "AsyncRedisBackend":
        """
        Context manager enter.
        """

        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Context manager exit.
        """

        await self.disconnect()
