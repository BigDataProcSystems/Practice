from threading import Thread, Barrier
import time
import random


NUM_WORKERS = 5


def run_task():
    """Simulate running task."""
    time.sleep(random.randint(1,5))


def run_worker_tasks(tid, barrier: Barrier):
    """Simulate running multiple tasks per worker with barrier."""
    for i in range(5):
        print("Worker {} Task {} started at {}".format(tid, i, time.time()))
        run_task()
        print("\tWorker {} Task {} completed at {}".format(tid, i, time.time()))
        barrier.wait()


def run_job():
    """Simulate running job with multiple workers."""
    BARRIER = Barrier(NUM_WORKERS, timeout=10)

    threads = list()

    for i in range(NUM_WORKERS):
        thread = Thread(target=run_worker_tasks, args=(i, BARRIER))
        thread.start()
        threads.append(thread)

    for i in range(NUM_WORKERS):
        threads[i].join()


if __name__ == "__main__":
    run_job()
