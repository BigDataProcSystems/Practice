import argparse
from threading import Thread

from sysprog_ipc_socket import run_server, run_client


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-s", "--server", action="store_true", help="Run the server.")
    parser.add_argument("-c", "--clients", action="store_true", help="Run clients.")
    args = parser.parse_args()

    if not args.server and not args.clients:
        parser.error("No arguments provided.")

    if args.server:
        print("server")
        run_server()
    elif args.clients:
        for i in range(5):
            client = Thread(target=run_client, args=(i,))
            client.start()

