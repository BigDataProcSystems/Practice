import os
import time
import random
import threading

from concurrent.futures import ProcessPoolExecutor


def run_task(task_id):
    print("Worker [PID={}, TID={}]: Task {}".format(
        os.getpid(), threading.current_thread().name, task_id))
    time.sleep(random.randint(0,3))
    return str(task_id).zfill(2)


NUM_WORKERS = 4

with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
    # async execution in order
    outputs = executor.map(run_task, range(100), chunksize=5)
    for output in outputs:
        print("Result:\n\t{}".format(output))

