import threading


def write(value):
    with open("value", "w") as f:
        f.write(value)


def read():
    with open("value", "r") as f:
        return f.readline()


def pay(lock):
    with lock:
        total = int(read())
        total -= 1
        write(str(total))


if __name__ == '__main__':

    balance = 100

    write(str(balance))

    lock = threading.Lock()

    threads = []
    for i in range(100):
        thread = threading.Thread(target=pay, args=(lock,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(read())
