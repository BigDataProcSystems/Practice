# Многопроцессные приложения

Сергей Ю. Папулин (papulin_bmstu@mail.ru)

### Содержание

- [Пререквизиты](#Пререквизиты)
- [Модуль `multiprocessing`](#Модуль-`multiprocessing`)
- [Примитивы синхронизации процессов](#Примитивы-синхронизации-процессов)
- [Межпроцессная коммуникация](#Межпроцессная-коммуникация)
- [Сравнение производительности многопоточных и многопроцессных приложений](#Сравнение-производительности-многопоточных-и-многопроцессных-приложений)
- [Асинхронное выполнение с `concurrent.futures`](#Асинхронное-выполнение-с-concurrent.futures)
- [Асинхронное выполнение с `asyncio`](#Асинхронное-выполнение-с-asyncio)
- [Источники](#Источники)

## Пререквизиты

- [Процессы, потоки и IPC в Python](sysprog_proc_thread.md)
- [Примитивы синхронизации потоков](sysprog_thread_primitives.md)

## Модуль `multiprocessing`


sysprog_multiprocessing.py
```python
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

```

sysprog_multiprocessing_class.py
```python
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
        worker = Worker(i, LOCK)
        worker.start()
        workers.append(worker)

    for i in range(NUM_WORKERS):
        workers[i].join()

```

sysprog_multiprocessing_global.py
```python
from multiprocessing import Process


def run_task(wid):
    global var
    for _ in range(10):
        var += 1
        print("[worker-{}] \tvar = {}".format(wid, var))


var = 10

if __name__ == "__main__":

    NUM_WORKERS = 4

    workers = list()

    for i in range(NUM_WORKERS):
        worker = Process(target=run_task, args=(i,))
        worker.start()
        workers.append(worker)

    for i in range(NUM_WORKERS):
        workers[i].join()

    print("[master] \tvar = {}".format(var))
```

## Примитивы синхронизации процессов

- lock
- condition
- event
- semaphore synchronization


## Межпроцессная коммуникация

Стандартные средства коммуникации:
- сокеты
- именованная каналы

### Pipe

sysprog_multiprocessing_pipe.py
```python
from multiprocessing import Process, Pipe
import time


def run_task_A(pipe):
    print("Running A...")
    for i in range(2, 5):
        time.sleep(1)
        pipe.send(i)
        print("[A] sent: {}".format(i))
        msg = pipe.recv()
        print("[A] received: {}".format(msg))
    pipe.close()


def run_task_B(pipe):
    print("Running B...")
    while pipe.poll(5):
        msg = pipe.recv()
        print("\t[B] received: {}".format(msg))
        pipe.send(msg**2)
        print("\t[B] sent: {}".format(msg**2))


PIPEA, PIPEB = Pipe()

worker_1 = Process(target=run_task_A, args=(PIPEA,))
worker_2 = Process(target=run_task_B, args=(PIPEB,))

worker_1.start()
worker_2.start()
worker_1.join()
worker_2.join()
```

```bash
pstree -p $PID
```

sysprog_multiprocessing_pipe_.py
```python
from multiprocessing import Process, Pipe, Lock
import time
import os


def run_worker(wid, lock, pipe):
    while True:
        with lock:
            msg = pipe.recv()
        if msg == -1:
            pipe.close()
            break
        print("\t[{}] received: {}".format(wid, msg))


if __name__ == "__main__":

    PIPEMASTER, PIPEWORKER = Pipe()

    NUM_WORKERS = 10
    LOCK = Lock()
    workers = list()

    # Run workers
    for i in range(NUM_WORKERS):
        worker = Process(target=run_worker, args=(i, LOCK, PIPEWORKER))
        worker.start()
        workers.append(worker)

    # Show PID for master process (parent)
    print("[master] PID = {}".format(os.getpid()))

    # Send messages to workers
    for i in range(100):
        PIPEMASTER.send(i)
        print("[master] sent: {}".format(i))
        time.sleep(1)

    # Stop workers
    for _ in range(10):
        PIPEMASTER.send(-1)

    # Wait for completion of workers
    for i in range(NUM_WORKERS):
        workers[i].join()
```

### Value и Array

sysprog_multiprocessing_value_race.py
```python
from multiprocessing import Process, Value


def run_task(wid, var: Value):
    for _ in range(10):
        # involve a read and write are not atomic
        var.value += 1
        print("[worker-{}] \tvar = {}".format(wid, var.value))


if __name__ == "__main__":

    VAR = Value("i", 10)
    NUM_WORKERS = 4

    workers = list()

    for i in range(NUM_WORKERS):
        worker = Process(target=run_task, args=(i, VAR))
        worker.start()
        workers.append(worker)

    for i in range(NUM_WORKERS):
        workers[i].join()

    print("[master] \tvar = {}".format(VAR.value))
```

sysprog_multiprocessing_value.py
```python
from multiprocessing import Process, Value
import ctypes


def run_task(wid, var: Value):
    for _ in range(10):
        with var.get_lock():
            var.value += 1
            print("[worker-{}] \tvar = {}".format(wid, var.value))


if __name__ == "__main__":

    VAR = Value(ctypes.c_int, 10)
    NUM_WORKERS = 4

    workers = list()

    for i in range(NUM_WORKERS):
        worker = Process(target=run_task, args=(i, VAR))
        worker.start()
        workers.append(worker)

    for i in range(NUM_WORKERS):
        workers[i].join()

    print("[master] \tvar = {}".format(VAR.value))
```

sysprog_multiprocessing_array.py
```python
from multiprocessing import Process, Array
import ctypes


def run_task(wid, array: Array, start, stop):
    for i in range(start, stop):
        array[i] = wid
        array[i] += 1


if __name__ == "__main__":

    ARR_SIZE = 20
    ARR = Array(ctypes.c_int, ARR_SIZE, lock=False)

    NUM_WORKERS = 10

    workers = list()

    batch_size = ARR_SIZE // NUM_WORKERS

    for i in range(NUM_WORKERS):
        start = i * batch_size
        stop = start + batch_size
        worker = Process(target=run_task, args=(i, ARR, start, stop))
        worker.start()
        workers.append(worker)

    for i in range(NUM_WORKERS):
        workers[i].join()

    print("[master] \tarray = {}".format(list(ARR)))
```

### Queue

```python
import time
import queue
from multiprocessing import Process, Queue


def producer(tid, tasks: Queue):
    for i in range(5):
        time.sleep(1)
        tasks.put("{}:{}".format(tid, i))


def consumer(tid, tasks: Queue):
    while True:
        try:
            task = tasks.get(timeout=5)
            print("Worker {} Task {} completed".format(tid, task))
        except queue.Empty:
            break
    print("Worker {} finished.".format(tid))


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

```

## Pool

```python
import os
import time
import random

from multiprocessing import Pool, current_process


NUM_WORKERS = 4


def run_task(task_id):
    print("{} [PID={}]: Task {}".format(
        current_process().name, os.getpid(), task_id))
    time.sleep(random.randint(1,5))
    return str(task_id).zfill(2)


def run_map():
    """
    Notes:
        - converts to list
        - waits until all tasks are completed and then continues
        the main thread
    """
    with Pool(NUM_WORKERS) as p:
        outputs = p.map(run_task, range(10), chunksize=5)
        print("Result:\n\t{}".format(outputs))


def run_map_async():
    """
    Notes:
        - converts to list
        - continues the main thread without waiting task completion
    """
    with Pool(NUM_WORKERS) as p:
        outputs = p.map_async(run_task, range(10))
        print("[output] = {}".format(outputs))

        for output in outputs.get():
            print(output)


def run_imap():
    """
    Notes:
        - uses iterator
        - result from a completed task is available immediately
        but preserving the order, so it can wait until previous tasks completed
        before returns its result, but doesn't wait for all tasks to complete
    """
    with Pool(NUM_WORKERS) as p:
        outputs = p.imap(run_task, range(10))
        for output in outputs:
            print(output)


def run_imap_unordered():
    """
    Notes:
        - uses iterator
        - result from a completed task is available immediately and
        the order doesn't matter
    """
    with Pool(NUM_WORKERS) as p:
        outputs = p.imap_unordered(run_task, range(10))
        for output in outputs:
            print(output)


if __name__ == "__main__":
    run_map()

```

```
ForkPoolWorker-1 [PID=3271]: Task 0
ForkPoolWorker-4 [PID=3274]: Task 2
ForkPoolWorker-2 [PID=3272]: Task 1
ForkPoolWorker-3 [PID=3273]: Task 3
ForkPoolWorker-1 [PID=3271]: Task 4
ForkPoolWorker-4 [PID=3274]: Task 5
ForkPoolWorker-3 [PID=3273]: Task 6
ForkPoolWorker-2 [PID=3272]: Task 7
ForkPoolWorker-1 [PID=3271]: Task 8
ForkPoolWorker-3 [PID=3273]: Task 9
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```


## Сравнение производительности многопоточных и многопроцессных приложений

```python
import threading
import multiprocessing
import argparse


NUM = 100000000
NUM_WORKERS = 4


def timeit(function):
    import time

    def _function(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        print("t[{}] = {}s".format(function.__name__, end - start))
        return result
    return _function


def run_task(num):
    a = 0
    for i in range(num):
        a += 1


def run_in_main_thread(num_workers):
    """Run tasks without concurrency."""
    num = NUM // num_workers
    for i in range(num_workers):
        run_task(num)


def run_workers(num_workers, worker_class):
    """Run tasks with concurrency."""
    num = NUM // num_workers
    workers = list()
    for i in range(num_workers):
        worker = worker_class(target=run_task, args=(num,))
        worker.start()
        workers.append(worker)
    for i in range(num_workers):
        workers[i].join()


@timeit
def run(num_workers, worker_class=None):
    if worker_class is None:
        run_in_main_thread(num_workers)
    else:
        run_workers(num_workers, worker_class)


def test(num_workers):
    print("Running tasks without concurrency...")
    run(num_workers)
    print("Running tasks with multiple threads [{}]...".format(num_workers))
    run(num_workers, threading.Thread)
    print("Running tasks with multiple processes [{}]...".format(num_workers))
    run(num_workers, multiprocessing.Process)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-n", "--num_workers", type=int, help="Number of workers.", default=NUM_WORKERS)
    args = parser.parse_args()
    test(args.num_workers)
```

## Асинхронное выполнение с `concurrent.futures`

### Потоки

sysprog_futures_thread.py
```python
import os
import time
import random
import threading

from concurrent.futures import Future, ThreadPoolExecutor


def run_task(task_id):
    print("Worker [PID={}, TID={}]: Task {}".format(
        os.getpid(), threading.current_thread().name, task_id))
    time.sleep(random.randint(1,5))
    return str(task_id).zfill(2)


def print_complete_state(result: Future):
    print("Callback result: {}".format(result.result()))


executor = ThreadPoolExecutor(max_workers=1)
output = executor.submit(run_task, 2)
# call async
output.add_done_callback(print_complete_state)
# wait for result
print(output.result())
print("Shut downing...")
executor.shutdown()
```
sysprog_futures_thread_pool.py
```python
import os
import time
import random
import threading

from concurrent.futures import Future, ThreadPoolExecutor


def run_task(task_id):
    print("Worker [PID={}, TID={}]: Task {}".format(
        os.getpid(), threading.current_thread().name, task_id))
    time.sleep(random.randint(0,1))
    return str(task_id).zfill(2)


def print_complete_state(result: Future):
    print("Task was completed.")
    print("Callback{}".format(result.result()))


NUM_WORKERS = 4

with ThreadPoolExecutor(max_workers=NUM_WORKERS, thread_name_prefix="thread") as executor:
    # async execution in order
    outputs = executor.map(run_task, range(10), chunksize=5)
    for output in outputs:
        print("Result:\n\t{}".format(output))
```

### Процессы

```python
import os
import time
import random
import threading

from concurrent.futures import Future, ProcessPoolExecutor


def run_task(task_id):
    print("Worker [PID={}, TID={}]: Task {}".format(
        os.getpid(), threading.current_thread().name, task_id))
    time.sleep(random.randint(0,3))
    return str(task_id).zfill(2)


def print_complete_state(result: Future):
    print("Task was completed.")
    print("Callback{}".format(result.result()))


NUM_WORKERS = 4

with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
    # async execution in order
    outputs = executor.map(run_task, range(10), chunksize=5)
    for output in outputs:
        print("Result:\n\t{}".format(output))

```

## Асинхронное выполнение с `asyncio`

sysprog_asyncio.py
```python
import asyncio
import random


async def run_task(task_id):
    await asyncio.sleep(random.randint(1,2))
    print("Task [{}] completed".format(task_id))
    return task_id


async def run_job():
    tasks = [run_task(i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    print(results)


async def run_job_alt():
    tasks = [run_task(i) for i in range(10)]
    for task_future in asyncio.as_completed(tasks):
        result = await task_future
        print(result)


asyncio.run(run_job_alt())

```


## Источники

- [The Python Standard Library. Concurrent Execution](https://docs.python.org/3.7/library/concurrency.html)
- [`asyncio` — Asynchronous I/O](https://docs.python.org/3.7/library/asyncio.html)