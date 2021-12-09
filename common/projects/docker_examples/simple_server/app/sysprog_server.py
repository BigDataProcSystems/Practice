import os
import argparse
import logging

from socket import socket, AF_INET, SOCK_STREAM


def _setup_logger(is_server=False):
    import sys
    log_path = sys.path[0] + "/" + "server" if is_server else "client" + ".log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ])


HOST = "0.0.0.0"
PORT = 9998


def server(host=HOST, port=PORT):
    print("Server [{}]".format(os.getpid()))
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024).decode()
        logging.info("received request [{}]".format(data))
        # reverse data
        conn.send(data[::-1].encode())


def client(data, host=HOST, port=PORT):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))
    sock.send(data.encode())
    reply = sock.recv(1024).decode()
    sock.close()
    logging.info("sent [{}] => received: [{}]".format(data, reply))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-s", "--server", action="store_true", help="Run the server.")
    parser.add_argument("-c", "--client", action="store_true", help="Run the client.")
    parser.add_argument("-a", "--host", type=str, default=HOST, help="Host address.")
    parser.add_argument("-p", "--port", type=int, default=PORT, help="Port number.")
    args = parser.parse_args()

    if args.server:
        print("Server")
        _setup_logger(is_server=True)
        server(args.host, args.port)
    elif args.client:
        print("Client")
        _setup_logger()
        while True:
            data = input()
            if not data:
                break
            client(data, args.host, args.port)
