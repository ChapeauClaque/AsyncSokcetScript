import socket

connection = socket.socket()
connection.connect(('localhost', 25000), )
connection.settimeout(30)

while True:
    connection.send(input().encode())
    try:
        request = connection.recv(4096)
    except socket.timeout:
        break
    if not request:
        break
    else:
        print(request.decode())
else:
    connection.close()
