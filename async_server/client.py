import socket

connection = socket.socket()
connection.connect(('localhost', 25000), )


while True:
    print('message to server: ', end='')
    connection.send(input().encode())
    try:
        request = connection.recv(4096)
    except ConnectionResetError:
        print('Server had terminated the connection')
        break
    if request:
        print(request.decode())
    else:
        connection.close()
        break
