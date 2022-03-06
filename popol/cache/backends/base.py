from abc import ABCMeta, abstractmethod
from datetime import timedelta
from typing import Any, Dict, Optional, Union

from popol.cache.serializers.base import BaseSerializer

DictStrAny = Dict[str, Any]


class BaseCacheBackend(metaclass=ABCMeta):
    """
    Base class for all cache backends.
    """

    def __init__(self, serializer: BaseSerializer, **kwargs) -> None:
        self.serializer = serializer
        self.kwargs: DictStrAny = kwargs
        self.client = None

    @abstractmethod
    def connect(self) -> "BaseCacheBackend":
        """
        Connect to the server.
        """

    @abstractmethod
    def disconnect(self) -> None:
        """
        Disconnect from the server.
        """

    @abstractmethod
    def get(self, key: Any) -> Any:
        """
        Get a value from the cache.
        """

    @abstractmethod
    def set(
        self, key: Any, value: Any, timeout: Optional[Union[int, timedelta]] = None
    ) -> None:
        """
        Set a value in the cache.
        """

    @abstractmethod
    def delete(self, key: Any) -> None:
        """
        Delete a value from the cache.
        """

    @abstractmethod
    def clear(self) -> None:
        """
        Clear the entire cache.
        """
