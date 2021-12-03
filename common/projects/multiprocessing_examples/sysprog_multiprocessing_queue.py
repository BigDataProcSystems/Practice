import time
import queue
from multiprocessing import Process, Queue


def producer(wid, tasks: Queue):
    for i in range(5):
        time.sleep(1)
        tasks.put("{}:{}".format(wid, i))


def consumer(wid, tasks: Queue):
    while True:
        try:
            task = tasks.get(timeout=5)
            print("Worker {} Task {} completed".format(wid, task))
        except queue.Empty:
            break
    print("Worker {} finished.".format(wid))


QUEUE = Queue()
NUM_PRODUCER_THREADS = 2
NUM_CONSUMER_THREADS = 4

workers = list()

for i in range(NUM_PRODUCER_THREADS):
    worker = Process(target=producer, args=(i, QUEUE))
    worker.start()
    workers.append(worker)

for i in range(NUM_CONSUMER_THREADS):
    worker = Process(target=consumer, args=(i, QUEUE))
    worker.start()
    workers.append(worker)

for worker in workers:
    worker.join()

