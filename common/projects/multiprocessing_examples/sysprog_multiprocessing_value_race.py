from multiprocessing import Process, Value


def run_task(wid, var: Value):
    for _ in range(100):
        # involve a read and write are not atomic
        var.value += 1
        print("[worker-{}] \tvar = {}".format(wid, var.value))


if __name__ == "__main__":

    VAR = Value("i", 10)
    NUM_WORKERS = 4

    workers = list()

    for i in range(NUM_WORKERS):
        worker = Process(target=run_task, args=(i, VAR))
        worker.start()
        workers.append(worker)

    for i in range(NUM_WORKERS):
        workers[i].join()

    print("[master] \tvar = {}".format(VAR.value))
