# Python ThreadPool Implementation

This project demonstrates a custom thread pool in Python, built from scratch using threading, a linked-list-based queue, and condition variables. It allows you to submit jobs (functions) for concurrent execution by a fixed number of worker threads.

## Features
- **Custom Thread-Safe Queue:** Implements a linked list queue with thread-safe enqueue and dequeue operations using locks and condition variables.
- **ThreadPool Class:** Manages worker threads, job submission, and graceful shutdown.
- **Graceful Shutdown:** Ensures all jobs finish and all threads exit cleanly on shutdown (Ctrl+C).
- **Job Submission:** Submit jobs interactively via user input; jobs are distributed among worker threads and run in parallel.

## How It Works
- Start the program. Each time you enter input and press Enter, a new job is submitted to the pool.
- Each job simulates work by sleeping for a random number of seconds and then prints a completion message.
- Up to 3 jobs run in parallel (configurable by changing the number of workers).
- Press Ctrl+C to shut down the pool and exit cleanly.

## Usage
1. Run the script:
   ```bash
   python main.py
   ```
2. Enter any input and press Enter to submit a job.
3. Repeat to submit more jobs.
4. Press Ctrl+C to shut down the thread pool and exit.

## Code Structure
- **Node:** Linked list node for the queue.
- **Queue:** Thread-safe queue for jobs, using a linked list and condition variable.
- **ThreadPool:** Manages worker threads, job submission, and shutdown.
- **job():** Example job function that simulates work.

## Requirements
- Python 3.7+

## Notes
- This implementation does not use Python's built-in `queue.Queue` or `concurrent.futures.ThreadPoolExecutor`—it is built from first principles for educational purposes.
- You can modify the `job()` function to run any callable.
- The number of worker threads can be changed by editing `ThreadPool(3)`.

---
Feel free to extend this project with more advanced features, such as job results, exception handling, or timeout support!
# Python-ThreadPool-Implementation
