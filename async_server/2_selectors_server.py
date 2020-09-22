import socket
import selectors

SELECT = selectors.DefaultSelector()


def connection_accept(server_socket: socket.socket):
    client_socket, ip_address = server_socket.accept()
    SELECT.register(fileobj=client_socket, events=selectors.EVENT_READ, data=transfer_data)
    print('Connection from', ip_address)


def transfer_data(client_socket: socket.socket):
    if request := client_socket.recv(4096):
        response = "I received {} bytes".format(len(request))
        client_socket.send(response.encode())
    else:
        close_connection(client_socket)


def close_connection(client_socket: socket.socket):
    print(f'Connection to {client_socket.getpeername()} closed')
    SELECT.unregister(client_socket)
    client_socket.close()


def event_loop():
    while True:
        events = SELECT.select()
        for key, _ in events:
            key.data(key.fileobj)


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 25000), )
    server.listen()
    SELECT.register(fileobj=server, events=selectors.EVENT_READ, data=connection_accept)
    event_loop()
