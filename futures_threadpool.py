import concurrent.futures
from threading import get_ident
import time
import random


def task(task_id):
    """Simulates a task that might fail"""
    time.sleep(1)  # Simulate work
    thread_id = get_ident()
    # Randomly fail some tasks
    if random.random() < 0.3:
        raise Exception(f"Task {task_id} failed in thread:{thread_id}!")

    return f"Task {task_id} completed successfully in thread:{thread_id}."


def main():
    # Create thread pool executor
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # Submit multiple tasks
        futures = []
        for i in range(5):
            future = executor.submit(task, i)
            futures.append(future)

        # Process results as they complete
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                print(f"Success: \n***{result}***\n in main thread")
            except Exception as e:
                print(f"Error:\n***{e}***\ndetected in main thread")


if __name__ == "__main__":
    main()