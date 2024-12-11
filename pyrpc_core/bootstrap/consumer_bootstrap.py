import inspect
import socket
import time
from typing import Type, Optional, Dict, Any
from ..registry.registry_config import RegistryConfig
from ..registry.registry_factory import RegistryFactory
from ..registry.registry import Registry, ServiceInstance
from ..protocol.protocol_message import ProtocolMessage
from ..protocol.protocol_constants import ProtocolConstants
from ..serializer.serializer_facotry import SerializerFactory


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
    
    def _handle_service_change(self, service_name: str, instances: list[ServiceInstance]):
        """
        Handle service change event
        """
        # update service instance cache
        self._service_instance[service_name] = instances

        print(f'Service chaged - {service_name}')
        print(f'Available instance pool: {len(instances)}')
        for instance in instances:
            print(f'Instance: {instance.host}:{instance.port}')

    def _create_service_proxy(self, consumer: ServiceConsumer) -> Any:
        """
        Create service proxy instance
        """
        service_methods = inspect.getmemebers(
            consumer.service_class,
            predicate=inspect.isfunction
        )

        class ServiceProxy:
            def __init__(self, bootstrap, consumer):
                self._bootstrap = bootstrap
                self._consumer = consumer

            def __getattr__(self, method_name):
                def invoke(*args, **kwargs):
                    instance = self._bootstrap._get_service_instance(self._consumer.service_name)
                    if not instance:
                        raise RuntimeError(f'No available instance for service: {self._consumer.service_name}')
                    
                    request = {
                        'service_name': self._consumer.service_name,
                        'method_name': method_name,
                        'parameter_types': [type(arg) for arg in args],
                        'args': args,
                        'kwargs': kwargs
                    }

                    return self._bootstrap._invoke_remote(instance, request)
                return invoke

        for method_name, method in service_methods:
            def create_proxy_method(name):
                def proxy_method(*args, **kwargs):
                    if not consumer.registry:
                        raise RuntimeError(f'No registry configured for service: {consumer.service_name}')
                    
                    instance = consumer.registry.get_instance(consumer.service_name)
                    if not instance:
                        raise RuntimeError(f'No available instance for service: {consumer.service_name}')
                    
                    request = {
                        'service_name': consumer.service_name,
                        'method_name': name,
                        'args': args,
                        'kwargs': kwargs
                    }

                    return self._invoke_remote(instance, request)
                return proxy_method
            setattr(ServiceProxy, method_name, create_proxy_method(method_name))
        return ServiceProxy(self, consumer)

    def _invoke_remote(self, instance: ServiceInstance, request: dict) -> Any:
        """
        Invoke remote service
        """
        try:
            protocol_message = ProtocolMessage(
                magic_numer=ProtocolConstants.MAGIC_NUMBER,
                version=ProtocolConstants.VERSION,
                serializer_type=ProtocolConstants.SERIALIZER_YAML,
                messge_type=ProtocolConstants.REQUEST_TYPE,
                compressor_type=ProtocolConstants.COMPRESSOR_NONE,
                request_id=int(time.time() * 1000),
                body = request
            )
            serializer = SerializerFactory.get_serializer(protocol_message.serializer_type)

            protocol_message.body = serializer.serialize(request)

            protocol_message.body = serializer.serialize(request)
            protocol_message.body_length = len(protocol_message.body)

            message_bytes = protocol_message.to_bytes()

            with socket.create_connection(
                (instance.host, instance.port),
                timeout=10
            ) as sock:
                sock.sendall(message_bytes)

                header_size = ProtocolMessage.get_header_length()
                header_data = sock.recv(header_size)
                if len(header_data) < header_size:
                    raise RuntimeError('Failed to receive complete header')
                
                response_message = ProtocolMessage.from_bytes(header_data)

                body_data = b''
                remaining = response_message.body_length
                while remaining > 0:
                    chunk = sock.recv(min(remaining, 4096))
                    if not chunk:
                        break
                    body_data += chunk
                    remainning -= len(chunk)
                
                if len(body_data) < response_message.body_length:
                    raise RuntimeError('Failed to receive complete message body')
                
                response_serializer = SerializerFactory.get_serializer(response_message.serializer_type)
                response = response_serializer.deserialize(body_data, dict)

                if response.get('status') == 'error':
                    raise RuntimeError(response.get('message', 'Unknown error'))
                
                return response.get('data')

        except Exception as e:
            print(f'Error invoking remote service: {e}')
            raise RuntimeError(f'Failed to invoke remote service: {e}')


    def _get_service_instance(self, service_name: str) -> Optional[ServiceInstance]:
        """
        Get service instance
        """
        return self._service_instance.get(service_name)
