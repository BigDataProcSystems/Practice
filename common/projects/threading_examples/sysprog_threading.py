import threading


# class CounterThread(threading.Thread):
#     def __init__(self, my_id, count, mutex):
#         self.my_id = my_id
#         self.count = count
#         self.mutex = mutex
#         threading.Thread.__init__(self)
#
#     def run(self):
#         for i in range(self.count):
#             time.sleep(1)
#             with self.mutex:
#                 print("[{}] => {}".format(self.my_id, i))


def run_task(tid, lock: threading.Lock):
    for i in range(10):
        lock.acquire()
        print("Task [{}] => {}".format(tid, i))
        lock.release()


if __name__ == "__main__":

    LOCK = threading.Lock()
    threads = []

    for i in range(5):
        thread = threading.Thread(target=run_task, args=(i, LOCK))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
