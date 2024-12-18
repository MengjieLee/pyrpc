import pytest
from pyrpc_core_example_common.model import User
from pyrpc_core_example_common.service.user_service import UserService
from pyrpc_core.registry import RegistryConfig
from pyrpc_core.bootstrap import ProviderBootstrap, ConsumerBootstrap

class UserServiceImpl(UserService):
    def __init__(self):
        self.users = []

    def get_user(self, id: int) -> User:
        return self.users.get(id)
    
    def create_user(self, user: User) -> bool:
        if user.id in self.users:
            return False
        self.users[user.id] = user
        return True
    
@pytest.fixture
def provider():
    registry_config = RegistryConfig(
        registry_type='memory',
        address='localhost:8000'
    )
    provider = ProviderBootstrap()
    provider.add_service(
        service_name='userService',
        service_instance=UserServiceImpl(),
        host='localhost',
        port=9000,
        registry_config=registry_config
    )
    provider.start()
    yield provider
    provider.stop()

@pytest.fixture
def consumer():
    registry_config = RegistryConfig(
        registry_type='memory',
        address='localhost:8000'
    )
    consumer = ConsumerBootstrap()
    consumer.add_service(
        service_name='userService',
        service_class=UserService,
        registry_config=registry_config
    )
    consumer.start()
    yield consumer
    consumer.stop()

def test_create_and_get_user(provider, consumer):
    user_service = consumer.get_service('userService')

    new_user = User(id=1, name='test', age=18)
    assert user_service.create_user(new_user) is True

    user = user_service.get_user(1)
    assert user == new_user
