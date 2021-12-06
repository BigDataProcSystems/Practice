import random
import time

from threading_examples.sysprog_threading_semaphore_decorator import concurrency


@concurrency(num_workers=10, limit=2)
def run_task():
    time.sleep(random.randint(1,3))


run_task()
