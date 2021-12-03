from multiprocessing import Process, Lock
import random
import time
import os


def run_task(pindx, lock: Lock):
    with lock:
        print("Worker {}: PID = {}".format(pindx, os.getpid()))
    time.sleep(random.randint(2,5))


if __name__ == "__main__":

    NUM_WORKERS = 10

    LOCK = Lock()
    workers = list()

    for i in range(NUM_WORKERS):
        worker = Process(target=run_task, args=(i, LOCK))
        worker.start()
        workers.append(worker)

    for i in range(NUM_WORKERS):
        workers[i].join()
