from abc import ABCMeta, abstractmethod
from typing import Any, Optional


class BaseSerializer(metaclass=ABCMeta):
    """
    Base class for all serializers.
    """

    def __init__(
        self, dumps_kwargs: Optional[dict] = None, loads_kwargs: Optional[dict] = None
    ):
        pass

    @abstractmethod
    def dumps(self, data: Any) -> Any:
        """
        Serialize the data.
        """

    @abstractmethod
    def loads(self, data: Any) -> Any:
        """
        Deserialize the data.
        """
