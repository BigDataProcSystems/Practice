import _thread as thread


def run_task(tid):
    for i in range(10):
        print("Task [{}] => {}".format(tid, i))
    finish_status[tid] = True


if __name__ == "__main__":

    NUM_TASK = 10
    finish_status = [False] * NUM_TASK  # [False, False,..., False]

    # Run tasks
    for i in range(NUM_TASK):
        thread.start_new_thread(run_task, (i,))

    # Wait for tasks to complete
    while False in finish_status:
        pass

    print("Job was completed.")