import os


count = 0


def child():
    global count
    count += 1
    print("Child process [{}]".format(os.getpid()))
    os._exit(count)
    print("Never reached.")


def parent():
    while True:
        newpid = os.fork()
        if newpid == 0:
            # Child process
            child()
        else:
            # Parent process
            pid, status = os.wait()
            print("Parent [{}] => Child [{}] status [{}] => [{}] "
                  .format(os.getpid(), pid, status, status >> 8))
        print(">>", end=" ")
        if input() == "q":
            break


if __name__ == '__main__':
    parent()
