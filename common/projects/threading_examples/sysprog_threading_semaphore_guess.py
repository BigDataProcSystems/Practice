import threading
import random
import time


def get_random_number():
    return random.randint(0, 9)


def guess_number(tid: int, target_number: int, lock: threading.Lock):
    time.sleep(1)
    number = get_random_number()
    with lock:
        if number == target_number:
            print("{}::Thread {} is WINNER!".format(time.time(), tid))
        else:
            print("{}::Thread {} is not winner :(".format(time.time(), tid))


def limit_processing(tid: int, target_number: int,
                     lock: threading.Lock,
                     semaphore: threading.Semaphore):
    with semaphore:
        guess_number(tid, target_number, lock)


if __name__ == "__main__":

    NUM_THREADS = 10
    LOCK = threading.Lock()
    SEMAPHORE = threading.Semaphore(5)

    target_number = get_random_number()
    threads = list()

    for i in range(NUM_THREADS):
        thread = threading.Thread(target=limit_processing,
                                  args=(i, target_number, LOCK, SEMAPHORE))
        thread.start()
        threads.append(thread)

    for i in range(NUM_THREADS):
        threads[i].join()