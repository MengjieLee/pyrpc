from pyrpc_easy_example.common.model import User
from pyrpc_easy_example.common.service import UserService
from pyrpc_easy.registry import LocalRegistry
from pyrpc_easy.server import RpcServer


class UserServiceImpl(UserService):
    def get_user(self, user: User) -> User:
        return User(name=f'Hello, {user.name}!')
    

def main():
    # Register service
    service = UserServiceImpl()
    LocalRegistry.register(UserService.__name__, service)

    # Start servcer
    server = RpcServer()
    server.serve_forever()


if __name__ == '__main__':
    main()
