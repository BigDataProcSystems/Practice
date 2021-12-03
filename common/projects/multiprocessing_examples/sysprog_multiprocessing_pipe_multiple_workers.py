from multiprocessing import Process, Pipe, Lock
import time
import os


def run_worker(wid, lock, pipe):
    while True:
        with lock:
            msg = pipe.recv()
        if msg == -1:
            pipe.close()
            break
        print("\t[{}] received: {}".format(wid, msg))


if __name__ == "__main__":

    PIPEMASTER, PIPEWORKER = Pipe()

    NUM_WORKERS = 10
    LOCK = Lock()
    workers = list()

    # Run workers
    for i in range(NUM_WORKERS):
        worker = Process(target=run_worker, args=(i, LOCK, PIPEWORKER))
        worker.start()
        workers.append(worker)

    # Show PID for master process (parent)
    print("[master] PID = {}".format(os.getpid()))

    # Send messages to workers
    for i in range(100):
        PIPEMASTER.send(i)
        print("[master] sent: {}".format(i))
        time.sleep(1)

    # Stop workers
    for _ in range(NUM_WORKERS):
        PIPEMASTER.send(-1)

    # Wait for completion of workers
    for i in range(NUM_WORKERS):
        workers[i].join()
