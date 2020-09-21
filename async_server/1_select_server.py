import socket
from select import select

SOCKETS = []


def connection_accept(server_socket: socket.socket):
    client_socket, ip_address = server_socket.accept()
    print('Connection from', ip_address)
    SOCKETS.append(client_socket)


def transfer_data(client_socket: socket.socket):
        if request := client_socket.recv(4096):
            response = "I received {} bytes".format(len(request))
            client_socket.send(response.encode())
        else:
            close_connection(client_socket)


def close_connection(client_socket: socket.socket):
    print(f'Connection to {client_socket.getpeername()} closed')
    SOCKETS.remove(client_socket)
    client_socket.close()


def event_loop():
    while True:
        reading_from_socket, _, _ = select(SOCKETS, [], [])
        for sock in reading_from_socket:
            if sock is server:
                connection_accept(sock)
            else:
                transfer_data(sock)


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 25000), )
    server.listen()
    SOCKETS.append(server)
    event_loop()
