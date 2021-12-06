import time
import random

from socket import socket, AF_INET, SOCK_STREAM


PORT = 9999
HOST = "localhost"


def run_server():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)
        reply = "server: received [{}]".format(data.decode())
        conn.send(reply.encode())
        print("server: processed [{}]".format(addr))


def run_client(tid):
    num = random.randint(0,2)
    time.sleep(num)
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.send("client [{}]: {}".format(tid, num).encode())
    reply = sock.recv(1024)
    sock.close()
    print("client [{}]: received [{}]".format(tid, reply.decode()))


if __name__ == "__main__":
    from threading import Thread
    server_thread = Thread(target=run_server)
    # don't wait for server thread
    server_thread.daemon = True
    server_thread.start()
    # do wait for clients to exit
    for i in range(5):
        client_thread = Thread(target=run_client, args=(i,))
        client_thread.start()
