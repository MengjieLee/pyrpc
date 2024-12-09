import json
from typing import Any
from .serializer import Serializer



class JsonSerializer(Serializer):

    def serialize(self, obj: Any) -> bytes:
        return json.dumps(obj, default=lambda o: o.__dict__).encode('utf-8')

    def deserialize(self, data: bytes, cls: type) -> Any:
        json_dict = json.loads(data.decode('utf-8'))
        if hasattr(cls, '__annotations__'):
            return cls(**json_dict)
        return json_dict
