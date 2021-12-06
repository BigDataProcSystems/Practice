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
# LOCK = Lock()
LOCK = RLock()

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
