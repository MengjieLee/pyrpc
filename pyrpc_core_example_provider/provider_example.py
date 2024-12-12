from pyrpc_core_example_common.service.user_service import UserService
from pyrpc_core_example_common.model.user import User
from pyrpc_core.registry.registry_config import RegistryConfig
from pyrpc_core.bootstrap.provider_bootstrap import ProviderBootstrap


class UserServiceImpl(UserService):

    def __init__(self):
        self.users = {}

    def get_user(self, id: int) -> User:
        if id not in self.users:
            raise ValueError(f'User not found: {id}')
        return self.users[id]
    
    def create_user(self, user: User) -> bool:
        if user.id in self.users:
            return False
        self.users[user.id] = user
        return True

def main():
    registry_config = RegistryConfig(
        registry_type='memrory',
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

    print('Provider started, press Ctrl+C to exit')
    try:
        pass
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        provider.stop()

if __name__ == '__main__':
    main()
