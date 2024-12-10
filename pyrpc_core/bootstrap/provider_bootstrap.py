from typing import Any, Optional, Dict
from ..registry.registry_config import RegistryConfig
from ..registry.registry import Registry, ServiceInstance
from ..registry.registry_factory import RegistryFactory
from ..protocol.protocol_constants import ProtocolConstants


class ServiceProvider:
    """
    Service provider class
    """
    
    def __init__(self,
                 service_name: str,
                 service_instance: Any,
                 host: str,
                 port: int,
                 registry_config: Optional[RegistryConfig] = None,
                 metadata: Dict[str, str] = None):
        self.service_name = service_name
        self.service_instance = service_instance
        self.host = host
        self.port = port
        self.registry_config = registry_config
        self.metadata: Optional[Registry] = None

        if registry_config:
            self.registry = RegistryFactory.get_registry(registry_config)


class ProviderBootstrap:
    """
    Provider bootstrap class
    """

    def __init__(self):
        self.providers: Dict[str, ServiceProvider] = {}

    def add_service(self,
                    service_name: str,
                    service_instance: Any,
                    host: str,
                    port: int,
                    registry_config: Optional[RegistryConfig] = None,
                    metadata: Dict[str, str] = None) -> 'ProviderBootstrap':
        provider = ServiceProvider(
            service_name=service_name,
            service_instance=service_instance,
            host=host,
            port=port,
            registry_config=registry_config,
            metadata=metadata
        )
        self.providers[service_name] = provider
        return self
    
    def start(self):
        """
        Start the provider bootstrap
        """
        try:
            for provider in self.providers.values():
                if provider.registry:
                    service_instance = ServiceInstance(
                        service_name=provider.service_name,
                        host=provider.host,
                        port=provider.port,
                        metadata={
                            'version': str(ProtocolConstants.VERSION),
                            'serializer': str(ProtocolConstants.SERIALIZER_YAML),
                            **provider.metadata
                        }
                    )
                    success = provider.registry.register(service_instance)
                    if not success:
                        raise RuntimeError(f'Failed to register service: {provider.service_name}')

            # TODO: Start RPC server
            self._start_rpc_server()
        except Exception as e:
            self.stop()
            raise RuntimeError(f'Failed to start provider bootstrap: {e}')
    
    def stop(self):
        try:
            for provider in self.providers.values():
                if provider.registry:
                    service_instance = ServiceInstance(
                        service_name=provider.service_name,
                        host=provider.host,
                        port=provider.port
                    )
                    provider.registry.unregister(service_instance)
            # TODO
            self._stop_rpc_server()
        except Exception as e:
            print(f'Error stopping provider bootstrap: {e}')
    
    def _start_rpc_server(self):
        pass
    
    def _stop_rpc_server(self):
        pass
