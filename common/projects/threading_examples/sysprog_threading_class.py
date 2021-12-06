import threading


class TaskThread(threading.Thread):
    def __init__(self, tid, lock):
        super().__init__()
        self.tid = tid
        self.lock = lock

    def run(self):
        for i in range(10):
            with self.lock:
                print("[{}] => {}".format(self.tid, i))


if __name__ == "__main__":

    LOCK = threading.Lock()
    threads = []

    for i in range(5):
        thread = TaskThread(i, LOCK)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
