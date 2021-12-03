from socket import socket, AF_INET, SOCK_STREAM


HOST = ""
PORT = 9998


def client(data):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.send(data.encode())
    reply = sock.recv(1024).decode()
    sock.close()
    print("sent [{}] => received: [{}]".format(data, reply))


if __name__ == "__main__":
    while True:
        data = input()
        if not data:
            break
        client(data)