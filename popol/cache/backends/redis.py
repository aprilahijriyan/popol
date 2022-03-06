from datetime import timedelta
from typing import Any, Optional, Union

from ..decorators import auto_connect
from ..serializers.base import BaseSerializer
from .base import BaseCacheBackend

try:
    from redis.client import Pipeline, Redis
    from redis.lock import Lock

except ImportError:
    errMsg = "Redis is not installed. Please install it with `pip install redis`"
    raise RuntimeError(errMsg)


class RedisBackend(BaseCacheBackend):
    """
    Redis cache backend.
    """

    def __init__(self, serializer: BaseSerializer, **kwargs):
        """
        Initialize the Redis cache.
        """

        super().__init__(serializer, **kwargs)
        self.client: Optional[Redis] = None

    def connect(self, **kwargs) -> "RedisBackend":
        """
        Create a connection to the Redis server.
        """

        if self.client:
            return self.client

        kwargs.update(self.kwargs)
        self.client = Redis(**kwargs)
        return self

    def disconnect(self) -> None:
        """
        Disconnect from the Redis server.
        """

        if self.client:
            self.client.close()
            self.client = None

    @auto_connect
    def get(self, key: str) -> Any:
        """
        Get a value from the cache.
        """

        value = self.client.get(key)
        if value:
            return self.serializer.loads(value)
        return value

    @auto_connect
    def set(
        self, key: str, value: Any, timeout: Optional[Union[int, timedelta]] = None
    ) -> None:
        """
        Set a value in the cache.
        """

        value = self.serializer.dumps(value)
        if timeout:
            self.client.setex(key, timeout, value)
        else:
            self.client.set(key, value)

    @auto_connect
    def delete(self, key: str) -> None:
        """
        Delete a value from the cache.
        """
        self.client.delete(key)

    @auto_connect
    def clear(self) -> None:
        """
        Clear the entire cache.
        """
        self.client.flushdb()

    @auto_connect
    def incr(self, name: str, amount: int = 1) -> int:
        """
        Increment the value of an integer cached key.
        """
        return self.client.incr(name, amount)

    @auto_connect
    def decr(self, name: str, amount: int = 1) -> int:
        """
        Decrement the value of an integer cached key.
        """
        return self.client.decr(name, amount)

    @auto_connect
    def pipeline(self, **kwds) -> Pipeline:
        return self.client.pipeline(**kwds)

    @auto_connect
    def lock(self, name: str, **kwds) -> Lock:
        return self.client.lock(name, **kwds)

    def __enter__(self) -> "RedisBackend":
        """
        Context manager enter.
        """

        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Context manager exit.
        """

        self.disconnect()
