from multiprocessing import Process, Pipe
import time


def run_task_A(pipe):
    """Send/receive data to/from process B."""
    print("Running A...")
    for i in range(2, 5):
        time.sleep(1)
        # Send data to B
        pipe.send(i)
        print("[A] sent: {}".format(i))
        # Receive data from B
        msg = pipe.recv()
        print("[A] received: {}".format(msg))
    # Close pipe A
    pipe.close()


def run_task_B(pipe: Pipe):
    """Receive/send data from/to process A."""
    print("Running B...")
    # Loop while data exists to receive, or wait for 5 seconds
    # and leave the loop
    while pipe.poll(5):
        # Receive data from A
        msg = pipe.recv()
        print("\t[B] received: {}".format(msg))
        # Send data to A
        pipe.send(msg**2)
        print("\t[B] sent: {}".format(msg**2))
    # Close pipe B
    pipe.close()


if __name__ == "__main__":

    # Create pipes
    PIPEA, PIPEB = Pipe()

    worker_1 = Process(target=run_task_A, args=(PIPEA,))
    worker_2 = Process(target=run_task_B, args=(PIPEB,))

    # Start processes
    worker_1.start()
    worker_2.start()

    # Note: Optionally you can close pipes in the parent process
    # as they are not used here
    PIPEA.close()
    PIPEB.close()

    # Wait for processes to complete
    worker_1.join()
    worker_2.join()
