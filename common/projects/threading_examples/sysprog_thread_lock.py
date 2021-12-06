import _thread as thread


def run_task(tid):
    for i in range(10):
        lock.acquire()
        print("Task [{}] => {}".format(tid, i))
        lock.release()
    finish_status[tid] = True


if __name__ == "__main__":

    NUM_TASK = 10

    lock = thread.allocate_lock()
    finish_status = [False] * NUM_TASK

    for i in range(NUM_TASK):
        thread.start_new_thread(run_task, (i,))

    while False in finish_status:
        pass

    print("Job was completed.")