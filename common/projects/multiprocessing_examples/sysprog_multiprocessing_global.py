from multiprocessing import Process


def run_task(wid):
    global var
    for _ in range(10):
        var += 1
        print("[worker-{}] \tvar = {}".format(wid, var))


var = 10

if __name__ == "__main__":

    NUM_WORKERS = 4

    workers = list()

    for i in range(NUM_WORKERS):
        worker = Process(target=run_task, args=(i,))
        worker.start()
        workers.append(worker)

    for i in range(NUM_WORKERS):
        workers[i].join()

    print("[master] \tvar = {}".format(var))
