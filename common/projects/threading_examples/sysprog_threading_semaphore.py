from threading import Thread, Lock, Semaphore
import random
import time


def run_task():
    time.sleep(random.randint(2,5))


def run_workers(tid, semaphore: Semaphore):
    semaphore.acquire()
    print("Starting {} worker at {}".format(tid, time.time()))
    run_task()
    semaphore.release()


if __name__ == "__main__":

    NUM_THREADS = 10
    SEMAPHORE = Semaphore(5)

    threads = list()

    for i in range(NUM_THREADS):
        thread = Thread(target=run_workers,
                        args=(i, SEMAPHORE))
        thread.start()
        threads.append(thread)

    for i in range(NUM_THREADS):
        threads[i].join()