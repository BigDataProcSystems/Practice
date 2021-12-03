import asyncio
import random
import threading
import argparse


async def run_task(task_id):
    """Simple coroutine."""
    print("Task")
    await asyncio.sleep(random.randint(1,3))
    print("[{}]: Task [{}] is completed."
          .format(threading.current_thread().name, task_id))
    return task_id


async def run_job_with_await():
    """
    Run concurrently and return a task result as completed.

    Note:
        - Behavior is different from that we saw before when tasks were ran as coroutines
        - Order doesn't matter here
    """
    tasks = list()
    for i in range(10):
        task = asyncio.create_task(run_task(i))
        tasks.append(task)
    print("Run")
    for task in tasks:
        # This is where a task is ran
        result = await task
        print("Result: [{}]".format(result))


async def run_job_with_wait():
    """
    Run concurrently and wait for all tasks to complete.

    Note: Order doesn't matter here
    """
    tasks = list()
    for i in range(10):
        task = asyncio.create_task(run_task(i))
        tasks.append(task)
    print("Run")
    # This is where all task are started
    tasks_done, tasks_pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    for future in tasks_done:
        print(future.result())


async def run_job_with_gather():
    """
    Run concurrently and wait for all tasks to complete.

    Note: Order does matter here
    """
    tasks = list()
    for i in range(10):
        task = asyncio.create_task(run_task(i))
        tasks.append(task)
    print("Run")
    # This is where all task are started
    # Note: gather(*[run_task(0), run_task(1)]) => gather(run_task(0), run_task(1))
    results = await asyncio.gather(*tasks)
    print(results)


async def run_job_with_as_completed():
    """
    Run concurrently and return a task result as completed.

    Note: Order doesn't matter here
    """
    tasks = list()
    for i in range(10):
        task = asyncio.create_task(run_task(i))
        tasks.append(task)
    print("Run")
    # This is where all task are started
    for task_future in asyncio.as_completed(tasks):
        result = await task_future
        print(result)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-a", "--await_loop", action="store_true", help="Run multiple task with await.")
    parser.add_argument("-w", "--wait", action="store_true", help="Run multiple task with wait.")
    parser.add_argument("-g", "--gather", action="store_true", help="Run multiple task with gather.")
    parser.add_argument("-c", "--as_completed", action="store_true", help="Run multiple task with completed.")
    args = parser.parse_args()

    coroutine = None

    if args.await_loop:
        coroutine = run_job_with_await()
    elif args.wait:
        coroutine = run_job_with_wait()
    elif args.gather:
        coroutine = run_job_with_gather()
    elif args.as_completed:
        coroutine = run_job_with_as_completed()

    # Create event loop, run a coroutine, close the loop.
    asyncio.run(coroutine)