from typing import Type, Optional, Dict, Any
from ..registry.registry_config import RegistryConfig
from ..registry.registry_factory import RegistryFactory
from ..registry.registry import Registry, ServiceInstance


class ServiceConsumer:

    def __init__(self,
                 service_name: str,
                 service_class: Type,
                 registry_config: Optional[RegistryConfig] = None):
        self.service_name = service_name
        self.service_class = service_class
        self.registry: Optional[Registry] = None
        self.proxy = None # proxy instance

        if registry_config:
            self.registry = RegistryFactory.get_registry(registry_config)


class ConsumerBootstrap:
    """
    Consumer bootstrap class
    """
    def __init__(self):
        self.consumers: Dict[str, ServiceConsumer] = {}
    
    def add_service(self,
                    service_name: str,
                    service_class: Type,
                    registry_config: Optional[RegistryConfig] = None) -> 'ConsumerBootstrap':
        consumer = ServiceConsumer(
            service_name=service_name,
            service_class=service_class,
            registry_config=registry_config
        )
        self.consumer[service_name] = consumer
        return self

    def start(self):
        try:
            for consumer in self.consumers.values():
                if consumer.registry:
                    consumer.registry.subscribe(
                        consumer.service_name,
                        self._handle_service_change
                    )
                consumer.proxy = self._create_service_proxy(consumer)
            pass
        except Exception as e:
            self.stop()
            raise RuntimeError(f'Failed to start consumer bootstrap: {e}')

    def stop(self):
        try:
            for consumer in self.consumers.values():
                if consumer.registry:
                    consumer.registry.unsubscribe(consumer.service_name)
            pass
        except Exception as e:
            print(f'Error stopping consumer bootstrap: {e}')
    
    def get_service(self, service_name: str) -> Any:
        if service_name not in self.consumers:
            raise ValueError(f'Service {service_name} not found')
        return self.consumers[service_name].proxy
    
    def _handle_service_change(self, instance: list[ServiceInstance]):
        pass

    def _create_service_proxy(self, consumer: ServiceConsumer) -> Any:
        pass
