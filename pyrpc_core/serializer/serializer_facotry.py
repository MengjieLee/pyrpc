from typing import Dict
from .serializer import Serializer
from ..protocol.protocol_constants import ProtocolConstants
from .json_serializer import JsonSerializer
from .yaml_serializer import YamlSerializer


class SerializerFactory:
    """
    Factory class for creating serializers
    """
    
    _serializers: Dict[int, Serializer] = {}

    @classmethod
    def get_serializer(cls, serializer_type: int) -> Serializer:
        """
        Get a serializer instance by its type
        """
        if serializer_type not in cls._serializers:
            if serializer_type == ProtocolConstants.SERIALIZER_JSON:
                cls._serializers[serializer_type] = JsonSerializer
            elif serializer_type == ProtocolConstants.SERIALIZER_YAML:
                cls._serializers[serializer_type] = YamlSerializer
            else:
                raise ValueError(f'Unsupported serializer type: {serializer_type}')
        return cls._serializers[serializer_type]
