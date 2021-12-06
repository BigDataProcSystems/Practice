import os


def main():
    """Create new child processes until `q`"""
    count = 0   # process counter
    while True:
        count += 1
        # create a child process
        pid = os.fork()
        if pid == 0:
            """Inside the child process"""
            os.execlp("python", "-c", "sysprog_exec_child.py", str(count))
        else:
            """Inside the parent process"""
            print("Parent [PID={}] creates: [{}] child process [PID={}]"
                  .format(os.getpid(), count, pid))
        # condition to stop
        if input() == "q":
            break


if __name__ == "__main__":
    main()
