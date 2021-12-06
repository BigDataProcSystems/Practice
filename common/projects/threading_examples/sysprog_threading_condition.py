import time
from threading import Thread, Condition


def producer(tid, tasks, cond: Condition):
    for i in range(5):
        time.sleep(1)
        with cond:
            tasks.append("{}:{}".format(tid, i))
            cond.notify()
            print(tasks)


def consumer(tid, tasks, cond: Condition):
    with cond:
        while True:
            cond.wait(timeout=5)
            if len(tasks) == 0:
                break
            task = tasks.pop(0)
            time.sleep(1)
            print("Worker {} Task {} completed".format(tid, task))
        print("Worker {} finished.".format(tid))


COND = Condition()
NUM_PRODUCER_THREADS = 2
NUM_CONSUMER_THREADS = 4

TASKS = list()
threads = list()

for i in range(NUM_PRODUCER_THREADS):
    thread = Thread(target=producer, args=(i, TASKS, COND))
    thread.start()
    threads.append(thread)

for i in range(NUM_CONSUMER_THREADS):
    thread = Thread(target=consumer, args=(i, TASKS, COND))
    thread.start()
    threads.append(thread)

for i in range(len(threads)):
    threads[i].join()