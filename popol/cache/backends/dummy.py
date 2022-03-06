from ..serializers.base import BaseSerializer
from .base import BaseCacheBackend


class DummyBackend(BaseCacheBackend):
    def __init__(self, serializer: BaseSerializer, **options):
        super().__init__(serializer, **options)

    def connect(self) -> "DummyBackend":
        pass

    def disconnect(self) -> None:
        pass

    def get(self, key):
        pass

    def set(self, key, value, timeout=None):
        pass

    def delete(self, key):
        pass

    def clear(self):
        pass
