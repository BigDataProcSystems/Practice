from multiprocessing import Process, Array
import ctypes


def run_task(wid, array: Array, start, stop):
    for i in range(start, stop):
        array[i] = wid
        array[i] += 1


if __name__ == "__main__":

    ARR_SIZE = 20
    ARR = Array(ctypes.c_int, ARR_SIZE, lock=False)

    NUM_WORKERS = 10

    workers = list()

    batch_size = ARR_SIZE // NUM_WORKERS

    for i in range(NUM_WORKERS):
        start = i * batch_size
        stop = start + batch_size
        worker = Process(target=run_task, args=(i, ARR, start, stop))
        worker.start()
        workers.append(worker)

    for i in range(NUM_WORKERS):
        workers[i].join()

    print("[master] \tarray = {}".format(list(ARR)))
