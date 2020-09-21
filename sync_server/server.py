import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 25000), )
server_socket.listen()

while True:
    client_socket, ip_address = server_socket.accept()
    client_socket.settimeout(5)
    print('Connection from', ip_address)
    while True:
        try:
            request = client_socket.recv(4096)
        except socket.timeout:
            break
        if not request:
            break
        else:
            print(request.decode())
            response = "I received {} bytes".format(len(request))
            client_socket.send(response.encode())
    print(f'Connection to {ip_address} closed')
    client_socket.close()
