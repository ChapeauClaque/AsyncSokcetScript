import socket

connection = socket.socket()
connection.connect(('localhost', 25000), )
connection.settimeout(5)

while True:
    connection.send(input().encode())
    try:
        request = connection.recv(4096)
    except socket.timeout:
        break
    except ConnectionAbortedError:
        print('Server had terminated the connection')
        break
    if not request:
        connection.close()
        break
    else:
        print(request.decode())
