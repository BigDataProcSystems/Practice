import asyncio
import argparse


HOST = "127.0.0.1"
PORT = 9996


async def client(message):
    reader, writer = await asyncio.open_connection(HOST, PORT)
    writer.write(message.encode())
    reply = await reader.read(1024)
    print("sent [{}] => received: [{}]".format(message, reply.decode()))
    writer.close()


async def handle_client(reader, writer):
    data = await reader.read(1024)
    message = data.decode()[::-1]
    addr = writer.get_extra_info("peername")
    print("client: {}".format(addr))
    writer.write(message.encode())
    await writer.drain()
    writer.close()


async def server():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print("serving on {}".format(addr))
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-s", "--server", action="store_true", help="Start the server.")
    parser.add_argument("-c", "--client", type=str, help="Start the client.")

    args = parser.parse_args()

    if args.server:
        print("Starting the server...")
        asyncio.run(server())
    elif args.client is not None:
        print("Starting the client...")
        asyncio.run(client(args.client))

