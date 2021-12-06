import threading
import time
import random


def start_job(event: threading.Event):
    print("Starting job...")
    event.set()


def run_task(tid, event: threading.Event):
    event.wait()
    time.sleep(random.randint(0,1))
    print("Worker {} Task completed at {}".format(tid, time.time()))


if __name__ == "__main__":

    NUM_THREADS = 10
    EVENT = threading.Event()

    threads = list()

    for i in range(NUM_THREADS):
        thread = threading.Thread(target=run_task, args=(i, EVENT))
        thread.start()
        threads.append(thread)

    print("Waiting", end="")
    for _ in range(5):
        time.sleep(1)
        print(".", end="")

    start_job(EVENT)

    for i in range(NUM_THREADS):
        threads[i].join()
