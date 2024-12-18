import pytest
from pyrpc_core.registry import RegistryConfig, MemoryRegistry
from pyrpc_core.registry.registry import ServiceInstance


@pytest.fixture
def registry():
    config = RegistryConfig(registry_type='memory', address='localhost:8000')
    return MemoryRegistry(config)

def test_register_and_unregister_service(registry):
    instance = ServiceInstance(
        service_name='testService',
        host='localhost',
        port=1234
    )
    
    assert registry.register(instance) is True
    assert len(registry.list_instances('testService')) == 1

    assert registry.unregister(instance) is True
    assert len(registry.list_instances('testService')) == 0

def test_get_instance(registry):
    instance1 = ServiceInstance(
        service_name='testService',
        host='localhost',
        port=1234
    )
    instance2 = ServiceInstance(
        service_name='testService',
        host='localhost',
        port=5678
    )
    registry.register(instance1)
    registry.register(instance2)

    instance = registry.get_instance('testService')
    assert instance in [instance1, instance2]
