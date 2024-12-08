from http.server import HTTPServer, BaseHTTPRequestHandler
from .serializer import Serializer, PickleSerializer
from .model import RpcRequest, RpcResponse
from .registry import LocalRegistry


class RpcHandler(BaseHTTPRequestHandler):
    serializer: Serializer = PickleSerializer()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        # Read the raw POST request data from the request's input stream (rfile)
        # The amount to read is specified by the Content-Length header
        post_data = self.rfile.read(content_length)

        try:
            # Deserialize the request
            request: RpcRequest = self.serializer.deserialize(post_data, RpcRequest)

            # Get service and call method
            service = LocalRegistry.get_service(request.service_name)
            method = getattr(service, request.method_name)
            result = method(*request.args)

            # Create and serialize the reponse
            response = RpcResponse(data=result)
            response_bytes = self.serializer.serialize(response)

            # Send the response
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.end_headers()
            # wfile: Simple writable BufferedIOBase implementation for a socket
            self.wfile.write(response_bytes)

        except Exception as e:
            response = RpcResponse(data=None, exception=e)
            response_bytes = self.serializer.serialize(response)
            self.send_response(500)
            self.send_header('Content-Type', 'application/octet-stream')
            self.end_headers()
            self.wfile.write(response_bytes)


class RpcServer:
    def __init__(self, host='127.0.0.1', port=8080):
        self.server = HTTPServer((host, port), RpcHandler)

    def serve_forever(self):
        print(f'Server running on {self.server.server_address}')
        self.server.serve_forever()
    