import socket
import threading
import pickle
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
        self.server_socket = socket.socket(socket.AF_INET, socket.SCOK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f'RPC Server started on {self.host}:{self.port}')

        self.running = True
        self.server_thread = threading.Thread(target=self._accept_clients, deamon=True)
        self.server_thread.start()

    def _accept_clients(self):
        while self.running:
            client_socket, addr = self.server_socket.accept()
            print(f'Accepted connection from {addr}')
            client_thread = threading.Thread(tartget=self._handle_client, args=(client_socket,), daemon=True)
            client_thread.start()

    def _handle_client(self, client_socket):
        try:
            while self.running:
                data = client_socket.recv(4096)
                if not data:
                    break
                request = pickle.loads(data)
                response = self._process_request(request)
                client_socket.sendall(pickle.dumps(response))
        except Exception as e:
            print(f'Error handling client: {e}')
        finally:
            client_socket.close()

    def _process_request(self, request: dict):
        try:
            service_name = request.get('service_name')
            method_name = request.get('method_name')
            args = request.get('args', [])
            kwargs = request.get('kwargs', {})

            provider = self.providers.get(service_name)
            if not provider:
                return {
                    'status': 'error',
                    'message': f'Service not found: {service_name}'
                }
            
            method = getattr(provider.service_instance, method_name, None)
            if not method:
                return {
                    'status': 'error',
                    'message': f'Method not found: {method_name}'
                }

            result = method(*args, **kwargs)
            return {
                'status': 'success',
                'data': result
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def _stop_rpc_server(self):
        self.running = False
        self.server_socket.close()
        self.server_thread.join()
