import time
from threading import Thread, Lock


def run_task(lock: Lock):
    global a
    for _ in range(10000000):
        with lock:
            a += 1
            a -= 1
        # lock.acquire()
        # try:
        #     a += 1
        #     a -= 1
        # finally:
        #     lock.release()


NUM_THREADS = 4
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
