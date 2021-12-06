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
