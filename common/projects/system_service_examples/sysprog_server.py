import os

from socket import socket, AF_INET, SOCK_STREAM


HOST = ""
PORT = 9998


def server():
    print("Server [{}]".format(os.getpid()))
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)
        print("received request [{}]".format(data))
        # reverse data
        conn.send(data.decode()[::-1].encode())


if __name__ == "__main__":
    server()
