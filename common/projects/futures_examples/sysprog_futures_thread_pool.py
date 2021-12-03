import os
import time
import random
import threading

from concurrent.futures import ThreadPoolExecutor


def run_task(task_id):
    print("Worker [PID={}, TID={}]: Task {}".format(
        os.getpid(), threading.current_thread().name, task_id))
    time.sleep(random.randint(0,1))
    return str(task_id).zfill(2)


NUM_WORKERS = 4

with ThreadPoolExecutor(max_workers=NUM_WORKERS, thread_name_prefix="thread") as executor:
    # async execution in order
    # run_task(0), run_task(1),..., run_task(9)
    outputs = executor.map(run_task, range(10), chunksize=5)
    for output in outputs:
        print("Result:\n\t{}".format(output))
