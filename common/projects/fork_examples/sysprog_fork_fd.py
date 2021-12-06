import os
import time


def child(fin):
    for i in range(10):
        time.sleep(1)
        fin.write(str(i) + "\n")
        fin.flush()
        # fin.seek(fin.tell()+1)
    fin.close()


def parent():
    """Sharing open file among processes"""

    fin = open(FILE_PATH, "w+")

    pid = os.getpid()
    print("Program:\t{}".format(pid))

    fd = fin.fileno()
    print("File Descriptor:", fd)

    child_pid = os.fork()
    if child_pid == 0:
        # Child process
        child(fin)
    else:
        # Parent process
        print("Child Process:\t{}".format(child_pid))
        for _ in range(10):
            print("Parent: {}".format(fin.tell()))
            time.sleep(1)
        fin.close()


FILE_PATH = "sysprog_fork_fd__sharedfile"


if __name__ == '__main__':
    parent()
