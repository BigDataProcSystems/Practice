import time
from threading import Thread
from queue import Queue, Empty


def producer(tid, tasks: Queue):
    for i in range(5):
        time.sleep(1)
        tasks.put("{}:{}".format(tid, i))


def consumer(tid, tasks: Queue):
    while True:
        try:
            task = tasks.get(timeout=5)
            print("Worker {} Task {} completed".format(tid, task))
        except Empty:
            break
    print("Worker {} finished.".format(tid))


QUEUE = Queue()
NUM_PRODUCER_THREADS = 2
NUM_CONSUMER_THREADS = 4

threads = list()

for i in range(NUM_PRODUCER_THREADS):
    thread = Thread(target=producer, args=(i, QUEUE))
    thread.start()
    threads.append(thread)

for i in range(NUM_CONSUMER_THREADS):
    thread = Thread(target=consumer, args=(i, QUEUE))
    thread.start()
    threads.append(thread)

for i in range(len(threads)):
    threads[i].join()
