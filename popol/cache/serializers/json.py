from datetime import datetime
from typing import Any, Optional, Union

from popol import json

from .base import BaseSerializer

JSON_TYPE = Union[dict, list]


class JSONSerializer(BaseSerializer):
    """
    JSON serializer.
    """

    def __init__(
        self, dumps_kwargs: Optional[dict] = None, loads_kwargs: Optional[dict] = None
    ):
        self.dumps_kwargs = dumps_kwargs or {}
        self.loads_kwargs = loads_kwargs or {}
        self.dumps_kwargs.setdefault("default", self.handler)

    def handler(self, o: Any):
        if isinstance(o, datetime):
            return str(o)
        elif hasattr(o, "serialize"):
            return o.serialize()
        raise TypeError(f"Type {type(o)} is not JSON serializable")

    def dumps(self, data: JSON_TYPE) -> str:
        """
        Serialize the data to a JSON string.
        """
        value = json.dumps(data, **self.dumps_kwargs)
        if isinstance(value, bytes):
            value = value.decode("utf-8")
        return value

    def loads(self, data: Union[str, bytes]) -> JSON_TYPE:
        """
        Deserialize a JSON string to a dictionary or list.
        """
        return json.loads(data, **self.loads_kwargs)
