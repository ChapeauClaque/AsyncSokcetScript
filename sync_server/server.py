import socket


class SyncServer(socket.socket):
    def __init__(self, ip_addr: str, port: int):
        super(SyncServer, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind((str(ip_addr), int(port)), )

    def run(self):
        self.listen()


def connection_accept(server_socket: SyncServer):
    client_socket, ip_address = server_socket.accept()
    client_socket.settimeout(5)
    print('Connection from', ip_address)
    transfer_data(client_socket)
    close_connection(client_socket)


def transfer_data(client_socket):
    while True:
        try:
            request = client_socket.recv(4096)
        except socket.timeout:
            return
        if not request:
            return
        else:
            print(request.decode())
            response = "I received {} bytes".format(len(request))
            client_socket.send(response.encode())


def close_connection(client_socket):
    print(f'Connection to {client_socket.getpeername()} closed')
    client_socket.close()


if __name__ == '__main__':
    server = SyncServer('localhost', 25000)
    server.run()
    while True:
        connection_accept(server)
