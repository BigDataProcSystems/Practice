import _thread as thread


def run_task(tid):
    print("Thread [{}]".format(tid))


def run_job():
    i = 0
    while True:
        i += 1
        thread.start_new_thread(run_task, (i,))
        if input() == "q":
            break


if __name__ == "__main__":
    run_job()
