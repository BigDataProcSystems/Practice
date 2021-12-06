import argparse
import os
import time
import random


def run_worker():
    pipeout = os.open(FIFO_PIPE_PATH, os.O_WRONLY)
    while True:
        num = random.randint(0, 3)
        time.sleep(num)
        os.write(pipeout, "Worker [{}]: {}\n".format(os.getpid(), num).encode())


def run_master():
    pipein = open(FIFO_PIPE_PATH, "r")
    while True:
        line = pipein.readline()[:-1]
        if not line:
            break
        print("Master [{}]: received [{}]".format(os.getpid(), line))


FIFO_PIPE_PATH = "sysprog_ipc_npipe__tmp"


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-m", "--master", action="store_true", help="Run the master.")
    parser.add_argument("-w", "--worker", action="store_true", help="Run the worker.")
    args = parser.parse_args()

    if not args.master and not args.worker:
        parser.error("No arguments provided.")

    if not os.path.exists(FIFO_PIPE_PATH):
        os.mkfifo(FIFO_PIPE_PATH)

    if args.master:
        print("Master")
        run_master()
    elif args.worker:
        print("Worker")
        run_worker()
