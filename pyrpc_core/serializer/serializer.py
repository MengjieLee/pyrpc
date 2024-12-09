from abc import ABC, abstractmethod
from typing import Any


class Serializer(ABC):
    """
    Base class for all serializers
    """

    @abstractmethod
    def serialize(self, obj: Any) -> bytes:
        pass

    @abstractmethod
    def deserialize(self, data: bytes, cls: type) -> Any:
        pass
