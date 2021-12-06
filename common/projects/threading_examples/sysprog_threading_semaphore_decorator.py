from threading import Thread, Semaphore
import time


def concurrency(num_workers=1, limit=1):
    def _concurrency(function):
        semaphore = Semaphore(limit)
        def _function(*args):
            def run_worker(tid, *args):
                with semaphore:
                    print("Worker {} started at {}".format(tid, time.time()))
                    function(*args)
            workers = list()
            for i in range(num_workers):
                worker = Thread(target=run_worker, args=(i,)+args)
                worker.start()
                workers.append(worker)
            for i in range(num_workers):
                workers[i].join()
            return
        return _function
    return _concurrency
