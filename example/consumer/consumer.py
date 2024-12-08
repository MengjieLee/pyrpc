import requests
from pyrpc.serializer import PickleSerializer
from example.common.model import User
from pyrpc.model import RpcRequest, RpcResponse
from example.common.service import UserService


def main():
    # Create serializer
    serializer = PickleSerializer()

    # Create request
    user = User(name='MJ')
    request = RpcRequest(
        service_name=UserService.__name__,
        method_name='get_user',
        parameter_types=[User],
        args=[user]
    )

    # Serialize request
    request_bytes = serializer.serialize(request)

    # Send request
    response = requests.post(
        'http://127.0.0.1:8080',
        data=request_bytes,
        headers={'Content-Type': 'application/octet-stream'}
    )

    # Handle response
    if response.status_code == 200:
        rpc_response: RpcResponse = serializer.deserialize(response.content, RpcResponse)
        result_user: User = rpc_response.data
        print(f'Response: {result_user.name}')
    else:
        print(f'Error: {response.status_code}')


if __name__ == '__main__':
    main()
