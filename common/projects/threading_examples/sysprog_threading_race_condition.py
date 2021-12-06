from threading import Thread
import time


def run_task():
    global a
    for _ in range(10000000):
        a += 1
        a -= 1


NUM_THREADS = 4

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