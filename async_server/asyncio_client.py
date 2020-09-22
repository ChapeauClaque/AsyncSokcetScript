import asyncio


async def client(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    while True:
        print('to server: ', end='')
        message_to_server = input().encode()
        if not message_to_server:
            print('Close the connection')
            writer.close()
            await writer.wait_closed()
            return

        writer.write(message_to_server)
        await writer.drain()

        response = await reader.read(4096)
        print('from server:', response.decode())


if __name__ == '__main__':
    asyncio.run(client('127.0.0.1', 25000))
