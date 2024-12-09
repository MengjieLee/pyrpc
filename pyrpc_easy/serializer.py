import pickle
from abc import ABC, abstractmethod
from typing import Any, Type


class Serializer(ABC):
    @abstractmethod
    def serialize(self, obj: Any) -> bytes:
        pass

    @abstractmethod
    def deserialize(self, data: bytes, cls: Type) -> Any:
        pass


class PickleSerializer(Serializer):
    def serialize(self, obj: Any) -> bytes:
        return pickle.dumps(obj)

    def deserialize(self, data: bytes, cls: Type) -> Any:
        return pickle.loads(data)
