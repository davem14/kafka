import socket


class TcpConnector:

    def __init__(self, host: str = 'localhost', port: int = 9092):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_details = (host, port)

    def __enter__(self):
        self.sock.connect(self.connection_details)
        return self.sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()

    def send(self, request: bytes):
        request_size_int = len(request)
        request_size_bytes = request_size_int.to_bytes(4, 'big')
        self.sock.send(request_size_bytes + request)

    def receive(self) -> bytes:
        resp_size_bytes = self.sock.recv(4)
        resp_size_int = int.from_bytes(resp_size_bytes, 'big')
        return self.sock.recv(resp_size_int)

    def send_and_receive(self, request: bytes) -> bytes:
        with self:
            self.send(request)
            return self.receive()
