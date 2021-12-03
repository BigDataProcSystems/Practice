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
    print("Callback result: {}\n".format(result.result()))


print(os.getpid())
executor = ThreadPoolExecutor(max_workers=1)
output = executor.submit(run_task, 2)
# call async
output.add_done_callback(print_complete_state)
# wait for result
print(output.result())
print("Shutting down...")
executor.shutdown()
