import yaml
from .serializer import Serializer
from typing import Any


class YamlSerializer(Serializer):
    
    def serialize(self, obj: Any) -> bytes:
        return yaml.safe_dump(obj, encoding='utf-8', allow_unicode=True)
    
    def deserialize(self, data: bytes, cls: type) -> Any:
        return yaml.safe_load(data)
