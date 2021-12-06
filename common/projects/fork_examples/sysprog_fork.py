import os


def child():
    print("Child process [{}]".format(os.getpid()))
    os._exit(0)


def parent():
    """Create new child processes until `q`"""
    while True:
        # create a child process
        pid = os.fork()
        if pid == 0:
            """Inside the child process"""
            child()
        else:
            """Inside the parent process"""
            print("Parent [PID={}] creates: child process [PID={}]"
                  .format(os.getpid(), pid))
            if input() == "q":
                break


if __name__ == "__main__":
    parent()