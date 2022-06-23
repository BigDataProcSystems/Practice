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
        # run_task(0), run_task(1), run_task(2), run_task(3), run_task(4)
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
    import argparse
    parser = argparse.ArgumentParser(description="")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-m", "--map", action="store_true")
    group.add_argument("-i", "--imap", action="store_true")
    group.add_argument("-u", "--imap_unordered", action="store_true")
    group.add_argument("-a", "--map_async", action="store_true")
    args = parser.parse_args()

    if args.map:
        print("map")
        run_map()
    elif args.imap:
        print("imap")
        run_imap()
    elif args.imap_unordered:
        print("imap unordered")
        run_imap_unordered()
    elif args.map_async:
        print("map async")
        run_map_async()