import os
import time
import random


def run_worker(pipe):
    """Should run in a child process."""
    while True:
        num = random.randint(0, 3)
        time.sleep(num)
        os.write(pipe, "Worker [{}]: {}\n".format(os.getpid(), num).encode())


def run_master():
    """Parent process."""
    # create pipes: one for the parent, the other for a child
    pipein, pipeout = os.pipe()
    if os.fork() == 0:
        """Inside a child process"""
        # close the pipein as it won't be used in a child process
        os.close(pipein)
        # run some processing in the child process
        run_worker(pipeout)
    else:
        """Inside the parent process"""
        # close the pipeout as it won't be used in the parent process
        os.close(pipeout)
        # open pipe as file to read data as string instead of bytes and
        # use file methods.
        pipein = os.fdopen(pipein)
        while True:
            line = pipein.readline()[:-1]
            print("Master [{}]: received [{}]".format(os.getpid(), line))


if __name__ == "__main__":
    run_master()
