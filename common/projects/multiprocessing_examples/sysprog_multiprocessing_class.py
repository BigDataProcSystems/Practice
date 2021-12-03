from multiprocessing import Process, Lock
import random
import time
import os


class Worker(Process):
    def __init__(self, pindex, lock: Lock):
        super().__init__()
        self.pindex = pindex
        self.lock = lock

    def run(self):
        with self.lock:
            print("Worker {}: PID = {}".format(self.pindex, os.getpid()))
        time.sleep(random.randint(2,5))


if __name__ == "__main__":

    NUM_WORKERS = 10

    LOCK = Lock()
    workers = list()

    for i in range(NUM_WORKERS):
        # Alternative to:
        # worker = Process(target=run_task, args=(i, LOCK))
        worker = Worker(i, LOCK)
        worker.start()
        workers.append(worker)

    for i in range(NUM_WORKERS):
        workers[i].join()

