import pickle
from typing import Any, Optional, Union

from .base import BaseSerializer


class PickleSerializer(BaseSerializer):
    """
    Pickle serializer.
    """

    def __init__(
        self, dumps_kwargs: Optional[dict] = None, loads_kwargs: Optional[dict] = None
    ):
        self.dumps_kwargs = dumps_kwargs or {}
        self.loads_kwargs = loads_kwargs or {}
        self.dumps_kwargs.setdefault("protocol", pickle.HIGHEST_PROTOCOL)

    def dumps(self, data: Any) -> bytes:
        if isinstance(data, int):
            return data

        return pickle.dumps(data, **self.dumps_kwargs)

    def loads(self, data: Union[bytes, int]) -> Any:
        try:
            return int(data)
        except ValueError:
            return pickle.loads(data, **self.loads_kwargs)
