# Threaded Job Scheduler with MinHeap

This project implements a simple threaded job scheduler in Python using a custom MinHeap for job scheduling. Jobs can be scheduled to run after a specified delay, and the system supports clean shutdown via Ctrl+C.

## Features
- **MinHeap-based Scheduling:** Jobs are stored in a min-heap, ordered by their scheduled execution time.
- **Producer-Consumer Model:**
  - The producer thread accepts user input to schedule jobs.
  - The consumer thread executes jobs at their scheduled time.
- **Thread-Safe:** Uses locks and condition variables to ensure safe concurrent access.
- **Graceful Shutdown:** Cleanly exits on Ctrl+C, ensuring all threads terminate properly.

## How It Works
- **Job Scheduling:**
  - Enter a number to schedule a job after that many seconds.
  - Enter a letter to schedule a job immediately.
- **Job Execution:**
  - The consumer thread waits for the next job's scheduled time and executes it.
  - Each job prints a random number after a random delay.

## Usage
1. Run the script:
   ```bash
   python main.py
   ```
2. Enter a number (e.g., `5`) to schedule a job after 5 seconds.
3. Enter a letter (e.g., `a`) to schedule a job immediately.
4. Press `Ctrl+C` to shut down the scheduler cleanly.

## Code Structure
- **MinHeap class:** Thread-safe min-heap for scheduling jobs.
- **producers:** Thread function to accept user input and schedule jobs.
- **consumers:** Thread function to execute jobs at their scheduled time.
- **Graceful shutdown:** Uses `threading.Event` and condition variables for clean exit.

## Requirements
- Python 3.7+

## Notes
- The producer thread may remain blocked on input during shutdown; this is a known limitation of Python's `input()` function.
- All jobs are simple functions that print a random number after a random delay.

---
Feel free to modify the job function or extend the scheduler for more complex use cases!