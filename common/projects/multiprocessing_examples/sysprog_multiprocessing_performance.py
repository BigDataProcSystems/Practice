import threading
import multiprocessing
import argparse


NUM = 100000000
NUM_WORKERS = 4


def timeit(function):
    import time

    def _function(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        print("t[{}] = {}s".format(function.__name__, end - start))
        return result
    return _function


def run_task(num):
    a = 0
    for i in range(num):
        a += 1


def run_in_main_thread(num_workers):
    """Run tasks without concurrency."""
    num = NUM // num_workers
    for i in range(num_workers):
        run_task(num)


def run_workers(num_workers, worker_class):
    """Run tasks with concurrency."""
    num = NUM // num_workers
    workers = list()
    for i in range(num_workers):
        worker = worker_class(target=run_task, args=(num,))
        worker.start()
        workers.append(worker)
    for i in range(num_workers):
        workers[i].join()


@timeit
def run(num_workers, worker_class=None):
    if worker_class is None:
        run_in_main_thread(num_workers)
    else:
        run_workers(num_workers, worker_class)


def test(num_workers):
    print("Running tasks without concurrency...")
    run(num_workers)
    print("Running tasks with multiple threads [{}]...".format(num_workers))
    run(num_workers, threading.Thread)
    print("Running tasks with multiple processes [{}]...".format(num_workers))
    run(num_workers, multiprocessing.Process)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-n", "--num_workers", type=int, help="Number of workers.", default=NUM_WORKERS)
    args = parser.parse_args()
    test(args.num_workers)
