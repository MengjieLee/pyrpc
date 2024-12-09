from typing import Dict
from .memory_registry import MemoryRegistry
from .registry import Registry
from .registry_config import RegistryConfig

class RegistryFactory:
    """
    Factory class for creating registry instances
    """

    # reflection to get all registry types
    _registry_types: Dict[str, type] = {
        'memory': MemoryRegistry
    }

    @classmethod
    def get_registry(cls, config: RegistryConfig) -> Registry:
        registry_class = cls._registry_types.get(config.registry_type.lower())
        if not registry_class:
            raise ValueError(f'Unsupported registry type: {config.registry_type}')
        return registry_class(config)
