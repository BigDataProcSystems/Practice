# Примитивы синхронизации потоков

Сергей Папулин (papulin_bmstu@mail.ru)

### Содержание

- [Состояние гонки и мьютексы](#Состояние-гонки-и-мьютексы)
- [Взаимная блокировка](#Взаимная-блокировка)
- [События](#События)
- [Барьеры](#Барьеры)
- [Семафоры](#Семафоры)
- [Условия](#Условия)
- [Очереди](#Очереди)
- ~~Таймер~~

## Состояние гонки и мьютексы

### Состояние гонки

sysprog_threading_race_condition.py
```python
from threading import Thread
import time


def run_task():
    global a
    for _ in range(1000000):
        a += 1
        a -= 1


NUM_THREADS = 2

threads = list()

a = 0

start_time = time.time()
for i in range(NUM_THREADS):
    thread = Thread(target=run_task, args=())
    thread.start()
    threads.append(thread)

for i in range(NUM_THREADS):
    threads[i].join()

print(time.time() - start_time)
print(a)
```

### Мьютекс

sysprog_threading_lock.py
```python
import time
from threading import Thread, Lock


def run_task(lock: Lock):
    global a
    for _ in range(1000000):
        with lock:
            a += 1
            a -= 1
        # lock.acquire()
        # try:
        #     a += 1
        #     a -= 1
        # finally:
        #     lock.release()

NUM_THREADS = 2
LOCK = Lock()

threads = list()

a = 0

start_time = time.time()
for i in range(NUM_THREADS):
    thread = Thread(target=run_task, args=(LOCK,))
    thread.start()
    threads.append(thread)

for i in range(NUM_THREADS):
    threads[i].join()
print(time.time() - start_time)
print(a)
```

### Рекурсивный мьютекс

sysprog_threading_rlock.py
```python
import time
from threading import Thread, Lock, RLock


def run_task(lock):
    global a
    for _ in range(1000000):
        with lock:
            with lock:
                a += 1
                a -= 1


NUM_THREADS = 2
LOCK = Lock()
# LOCK = RLock()

threads = list()

a = 0

start_time = time.time()
for i in range(NUM_THREADS):
    thread = Thread(target=run_task, args=(LOCK,))
    thread.start()
    threads.append(thread)

for i in range(NUM_THREADS):
    threads[i].join()
print(time.time() - start_time)
print(a)
```

## Взаимная блокировка

sysprog_threading_deadlock.py
```python
from threading import Thread, Lock


def run_task_A(lock1: Lock, lock2: Lock):
    global a, b
    for _ in range(100000):
        lock1.acquire(timeout=10)
        a += 1
        lock2.acquire(timeout=10)
        b += 1
        lock2.release()
        lock1.release()


def run_task_B(lock1: Lock, lock2: Lock):
    global a, b
    for _ in range(100000):
        lock2.acquire(timeout=10)
        b += 1
        lock1.acquire(timeout=10)
        a += 1
        lock1.release()
        lock2.release()


a = 0
b = 0

LOCK_1 = Lock()
LOCK_2 = Lock()

threadA = Thread(target=run_task_A, args=(LOCK_1, LOCK_2))
threadB = Thread(target=run_task_B, args=(LOCK_1, LOCK_2))
threadA.start()
threadB.start()
threadA.join()
threadB.join()
```

## События

sysprog_threading_event.py

```python
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
```


## Барьеры

sysprog_threading_barrier.py

```python
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
```

## Семафоры

sysprog_threading_semaphore.py

```python
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
```

sysprog_threading_semaphore_guess.py

```python
import threading
import random
import time


def get_random_number():
    return random.randint(0, 9)


def guess_number(tid: int, target_number: int, lock: threading.Lock):
    time.sleep(1)
    number = get_random_number()
    with lock:
        if number == target_number:
            print("{}::Thread {} is WINNER!".format(time.time(), tid))
        else:
            print("{}::Thread {} is not winner :(".format(time.time(), tid))


def limit_processing(tid: int, target_number: int,
                     lock: threading.Lock,
                     semaphore: threading.Semaphore):
    with semaphore:
        guess_number(tid, target_number, lock)


if __name__ == "__main__":

    NUM_THREADS = 10
    LOCK = threading.Lock()
    SEMAPHORE = threading.Semaphore(5)

    target_number = get_random_number()
    threads = list()

    for i in range(NUM_THREADS):
        thread = threading.Thread(target=limit_processing,
                                  args=(i, target_number, LOCK, SEMAPHORE))
        thread.start()
        threads.append(thread)

    for i in range(NUM_THREADS):
        threads[i].join()
```

### Декоратор

sysprog_threading_semaphore_decorator.py

```python
from threading import Thread, Semaphore
import time


def concurrency(num_workers=1, limit=1):
    def _concurrency(function):
        semaphore = Semaphore(limit)
        def _function(*args):
            def run_worker(tid, *args):
                with semaphore:
                    print("Worker {} started at {}".format(tid, time.time()))
                    function(*args)
            workers = list()
            for i in range(num_workers):
                worker = Thread(target=run_worker, args=(i,)+args)
                worker.start()
                workers.append(worker)
            for i in range(num_workers):
                workers[i].join()
            return
        return _function
    return _concurrency
```

sysprog_threading_semaphore_with_decorator.py

```python
import random
import time

from sysprog_threading_semaphore_decorator import concurrency


@concurrency(num_workers=10, limit=2)
def run_task():
    time.sleep(random.randint(1,3))


run_task()
```

## Условия

sysprog_threading_condition.py

```python
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
```

## Очереди

sysprog_threading_queue.py

```python
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
```


## Таймеры

```bash
# TODO
```

## Источники


[The Python Standard Library. Concurrent Execution](https://docs.python.org/3.7/library/concurrency.html)
