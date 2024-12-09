import redis
import json
from .registry import Registry, ServiceInstance
from .registry_config import RegistryConfig
from typing import List, Callable, Optional


class RedisRegistry(Registry):
    """
    Redis registry is a registry that uses Redis as the underlying storage.
    """

    SERVICE_PREFIX = 'pyrpc:service:'
    HEARTBEAT_PREFIX = 'pyrpc:heartbeat:'
    SERVICE_TTL = 30

    def __init__(self, config: RegistryConfig):
        super().__init__(config)
        self._redis = redis.Redis(
            host=config.address.split(':')[0],
            port=int(config.address.split(':')[1]),
            username=config.username,
            password=config.password,
            decode_responses=True
        )
        self._start_heartbeat_check()
    
    def register(self, service_instance: ServiceInstance) -> bool:
        try:
            instance_key = self._get_instance_key(service_instance)
            service_key = self._get_service_key(service_instance.service_name)

            instance_info = {
                'host': service_instance.host,
                'port': service_instance.port,
                'metadata': service_instance.metadata
            }

            pipeline = self._redis.pipeline()
            pipeline.hset(service_key, instance_key, json.dumps(instance_info))
            pipeline.set(
                self._get_heartbeat_key(instance_key),
                '1',
                ex=self.SERVICE_TTL
            )
            pipeline.execute()
            return True
        except Exception as e:
            print(f'Failed to register service: {e}')
            return False

    def unregister(self, service_instance: ServiceInstance) -> bool:
        try:
            instance_key = self._get_instance_key(service_instance)
            service_key = self._get_service_key(service_instance.service_name)

            pipeline = self._redis.pipeline()
            pipeline.hdel(service_key, instance_key)
            pipeline.delete(self._get_heartbeat_key(instance_key))
            pipeline.execute()
            return True
        except Exception as e:
            print(f'Failed to unregister service: {e}')
            return False

    def list_instances(self, service_name: str) -> List[ServiceInstance]:
        result = []
        try:
            service_key = self._get_service_key(service_name)
            instances = self._redis.hgetall(service_key)

            for instance_key, instance_info in instances.items():
                info = json.loads(instance_info)
                if self._is_instance_alive(instance_key):
                    result.append(ServiceInstance(
                        service_name=service_name,
                        host=info['host'],
                        port=info['port'],
                        metadata=info.get('metadata', {})
                    ))
        except Exception as e:
            print(f'Failed to list instances: {e}')
        return result
    
    def get_instance(self, service_name: str) -> Optional[ServiceInstance]:
        instances = self.list_instances(service_name)
        return instances[0] if instances else None

    def subscribe(self, service_name: str, callback: Callable) -> None:
        
        pass

    def unsubscribe(self, service_name: str) -> None:
        pass

    def _get_service_key(self, service_name: str) -> str:
        return f'{self.SERVICE_PREFIX}{service_name}'

    def _get_instance_key(self, instance: ServiceInstance) -> str:
        return f'{instance.host}:{instance.port}'

    def _get_heartbeat_key(self, instance_key: str) -> str:
        return f'{self.HEARTBEAT_PREFIX}{instance_key}'

    def _is_instance_alive(self, instance_key: str) -> bool:
        return bool(self._redis.exists(self._get_heartbeat_key(instance_key)))

    def _start_heartbbeat_check(self):
        pass
