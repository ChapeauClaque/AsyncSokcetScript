import socket
from select import select

TASKS = []
TO_READ = {}
TO_WRITE = {}


def connection_accept(server_socket: socket.socket):
    while True:
        yield ('read', server_socket)
        client_socket, ip_address = server_socket.accept()
        print('Connection from', ip_address)
        TASKS.append(transfer_data(client_socket))


def transfer_data(client_socket: socket.socket):
    while True:
        yield ('read', client_socket)
        request = client_socket.recv(4096)
        if request:
            response = "I received {} bytes".format(len(request))
            yield ('write', client_socket)
            client_socket.send(response.encode())
        else:
            close_connection(client_socket)
            return


def close_connection(client_socket: socket.socket):
    print(f'Connection to {client_socket.getpeername()} closed')
    client_socket.close()


def event_loop():
    while any([TASKS, TO_READ, TO_WRITE]):
        while not TASKS:
            read, write, _ = select(TO_READ, TO_WRITE, [])
            for sock in read:
                TASKS.append(TO_READ.pop(sock))
            for sock in write:
                TASKS.append(TO_WRITE.pop(sock))
        try:
            task = TASKS.pop(0)
            event, sock = next(task)
            if event == 'read':
                TO_READ[sock] = task
            elif event == 'write':
                TO_WRITE[sock] = task
        except StopIteration:
            print('Done!')


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 25000), )
    server.listen()
    TASKS.append(connection_accept(server))
    event_loop()