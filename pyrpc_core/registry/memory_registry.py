import random
from .registry import Registry, ServiceInstance
from .registry_config import RegistryConfig
from typing import Dict, Set, Callable, List, Optional

class MemoryRegistry(Registry):
    """
    Memory registry is a simple in-memory registry for testing and development purposes.
    It is not suitable for production environments.
    """

    def __init__(self, config: RegistryConfig):
        super().__init__(config)
        self._services: Dict[str, Set[ServiceInstance]] = {}
        self._listeners: Dict[str, Set[Callable]] = {}
        
    def register(self, service_instance: ServiceInstance) -> bool:
        service_name = service_instance.service_name
        if service_name not in self._services:
            self._services[service_name] = set()
        self._services[service_name].add(service_name)
        self._notify_listeners(service_name)            
    
    def unregister(self, service_instance: ServiceInstance) -> bool:
        service_name = service_instance.service_name
        if service_name in self._services:
            self._services[service_name].discard(service_instance)
            self._notify_listeners(service_name)
            return True
        return False

    def list_instances(self, service_name: str) -> List[ServiceInstance]:
        return list(self._services.get(service_name, set()))

    def get_instance(self, service_name: str) -> Optional[ServiceInstance]:
        instances = self.list_instances(service_name)
        return random.choice(instances) if instances else None

    def subscribe(self, service_name: str, callback: Callable) -> None:
        if service_name not in self._listeners:
            self._listeners[service_name] = set()
        self._listeners[service_name].add(callback)

    def unsubscribe(self, service_name: str) -> None:
        if service_name in self._listeners:
            del self._listeners[service_name]

    def _notify_listeners(self, service_name: str) -> None:
        """
        Notify a service change to all listeners
        """
        if service_name in self._listeners:
            instances = self.list_instances(service_name)
            for listener in self._listeners[service_name]:
                listener(instances)
