import asyncio
import random


async def run_task():
    await asyncio.sleep(random.randint(0,2))
    return True


async def run_job_with_error():
    try:
        result = await asyncio.wait_for(run_task(), 1)
        if result:
            print("Task is completed.")
    except asyncio.TimeoutError:
        """cancel task and raise exception"""
        print("Timeout error.")

if __name__ == "__main__":
    asyncio.run(run_job_with_error())
